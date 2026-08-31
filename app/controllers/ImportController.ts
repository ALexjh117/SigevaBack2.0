/* eslint-disable @unicorn/filename-case */
// ImportExcelController.ts (parcheado - devuelve processed por fila)
import type { HttpContext } from '@adonisjs/core/http'
import Aprendiz from '#models/aprendiz'
import Perfil from '#models/perfil'
import Grupo from '#models/grupo'
import ProgramaFormacion from '#models/programa_formacion'
import NivelFormacion from '#models/nivel_formacion'
import db from '@adonisjs/lucid/services/db'
import bcrypt from 'bcrypt'
import XLSX from 'xlsx'

import { resolverActor } from '#services/actor_sesion'
import {
  normalizarDocumento,
  normalizarEmail,
  parseFichaCaracterizacion,
} from '#services/import_ficha'

export default class ImportExcelController {
  public async importarAprendices({ request, response }: HttpContext) {
    const trx = await db.transaction()

    try {
      // Inicializar contadores
      let inserted = 0
      let updated = 0
      let skipped = 0
      let skippedAprendices: any[] = []

      // Nuevo: array con resultado procesado por fila (útil para frontend)
      const processed: Array<{
        'Número de Documento': string
        'Correo Electrónico': string
        'Nombre': string
        'Apellidos': string
        'status': 'inserted' | 'updated' | 'skipped'
        'motivo'?: string
      }> = []

      // 1) Actor: x-user-id o userId (HU-S2-030). Sin JWT.
      const actor = await resolverActor(request)
      if (!actor) {
        await trx.rollback()
        return response.badRequest({ success: false, message: 'Falta userId en el body o x-user-id' })
      }

      if (!actor.esDeCentro && !actor.esAdministrador) {
        await trx.rollback()
        return response.forbidden({
          success: false,
          message: 'Solo administradores, admin_sistema o funcionarios pueden importar aprendices',
        })
      }

      // Centro: sesión para funcionario y admin_sistema. El Administrador de red sí elige.
      let centroFormacionId: number | null = null
      if (actor.esDeCentro) {
        centroFormacionId = actor.idcentro
        if (!centroFormacionId) {
          await trx.rollback()
          return response.badRequest({
            success: false,
            message: 'Tu usuario no tiene centro de formación asignado',
          })
        }
        const bodyCentro = Number(request.input('centroFormacionId'))
        if (bodyCentro && bodyCentro !== centroFormacionId) {
          await trx.rollback()
          return response.forbidden({
            success: false,
            message: 'No puedes importar aprendices en otro centro de formación',
          })
        }
      } else {
        const bodyCentro = Number(request.input('centroFormacionId'))
        if (!bodyCentro) {
          await trx.rollback()
          return response.badRequest({
            success: false,
            message: 'Debes enviar centroFormacionId en el body (administrador)',
          })
        }
        centroFormacionId = bodyCentro
      }

      // Leer flag updateIfExists
      const updateIfExistsRaw = request.input('updateIfExists')
      const updateIfExists =
        updateIfExistsRaw === undefined
          ? true
          : updateIfExistsRaw === '1' || updateIfExistsRaw === 1 || updateIfExistsRaw === true

      // 2) Archivo y params
      const file = request.file('excel')

      if (!file) {
        await trx.rollback()
        return response.status(400).json({
          success: false,
          message: 'Debes subir un archivo Excel',
        })
      }

      // 3) Leer Excel — reporte Sofia Plus: C2 = "ficha - programa", filas desde la 5
      const workbook = XLSX.read(file.tmpPath, { type: 'file' })
      const sheet = workbook.Sheets[workbook.SheetNames[0]]

      const { numeroGrupo, nombrePrograma } = parseFichaCaracterizacion(sheet['C2']?.v)

      if (!numeroGrupo || !nombrePrograma) {
        await trx.rollback()
        return response.status(400).json({
          success: false,
          message:
            'No se encontró la ficha de caracterización o el programa en C2. Usa el Reporte de Aprendices de Sofia Plus sin cambiar el formato.',
        })
      }

      const data: any[] = XLSX.utils.sheet_to_json(sheet, { range: 4, defval: '' })

      // Recolectar documentos y correos
      const docsSet = new Set<string>()
      const emailsSet = new Set<string>()
      const filasProcesables: any[] = []

      for (const fila of data) {
        const numeroDocumento = normalizarDocumento(fila['Número de Documento'])
        const email = normalizarEmail(fila['Correo Electrónico'])

        if (!numeroDocumento && !email) continue

        filasProcesables.push({ fila, numeroDocumento, email })
        if (numeroDocumento) docsSet.add(numeroDocumento)
        if (email) emailsSet.add(email)
      }

      if (filasProcesables.length === 0) {
        await trx.commit()
        return response.ok({
          success: true,
          message: 'No hay filas válidas',
          inserted: 0,
          updated: 0,
          skipped: 0,
          skippedAprendices: [],
          processed: [],
        })
      }

      // Perfil canónico. No se crea un quinto rol ni se duplica Aprendiz.
      const perfil = await Perfil.query({ client: trx }).where('perfil', 'Aprendiz').first()
      if (!perfil) {
        await trx.rollback()
        return response.status(500).json({
          success: false,
          message: 'El perfil "Aprendiz" no existe. Créalo en la tabla perfil antes de importar.',
        })
      }

      let nivel = await NivelFormacion.query({ client: trx }).where('nivel_formacion', 'Técnico').first()
      if (!nivel) {
        nivel = new NivelFormacion()
        nivel.nivel_formacion = 'Técnico'
        await nivel.useTransaction(trx).save()
      }

      const AREA_SOFTWARE_ID = 1

      let grupo = await Grupo.query({ client: trx }).where('grupo', numeroGrupo).first()
      if (!grupo) {
        grupo = new Grupo()
        grupo.grupo = numeroGrupo
        grupo.jornada = ''
        await grupo.useTransaction(trx).save()
      }

      let programa = await ProgramaFormacion.query({ client: trx })
        .whereRaw("LOWER(REGEXP_REPLACE(TRIM(programa), '\\.+$', '')) = ?", [
          nombrePrograma.toLowerCase(),
        ])
        .first()
      if (!programa) {
        programa = new ProgramaFormacion()
        Object.assign(programa, {
          programa: nombrePrograma,
          idnivel_formacion: nivel.idnivel_formacion,
          idarea_tematica: AREA_SOFTWARE_ID,
          codigo_programa: 'N/A',
          version: '1.0',
          duracion: 0,
        })
        await programa.useTransaction(trx).save()
      }

      // ----------------- FILTRO DE DUPLICADOS DENTRO DEL MISMO EXCEL -----------------
      const seenDocs = new Set<string>()
      const seenEmails = new Set<string>()
      const filasUnicas: any[] = []

      for (const item of filasProcesables) {
        const { numeroDocumento, email, fila } = item
        if (
          (numeroDocumento && seenDocs.has(numeroDocumento)) ||
          (email && seenEmails.has(email))
        ) {
          skipped++
          const motivo = 'Duplicado en el Excel'
          skippedAprendices.push({
            'Número de Documento': numeroDocumento || '',
            'Correo Electrónico': email || '',
            'Nombre': fila['Nombre'] || '',
            'Apellidos': fila['Apellidos'] || '',
            'motivo': motivo,
          })
          // También registrar en processed para trazabilidad
          processed.push({
            'Número de Documento': numeroDocumento || '',
            'Correo Electrónico': email || '',
            'Nombre': fila['Nombre'] || '',
            'Apellidos': fila['Apellidos'] || '',
            'status': 'skipped',
            motivo,
          })
          continue
        }
        if (numeroDocumento) seenDocs.add(numeroDocumento)
        if (email) seenEmails.add(email)
        filasUnicas.push(item)
      }

      // ----------------- PROCESAR FILAS ÚNICAS -----------------
      for (const item of filasUnicas) {
        const { fila, numeroDocumento, email } = item
        const tipoDocumento = fila['Tipo de Documento'] || ''
        const nombres = fila['Nombre'] || ''
        const apellidos = fila['Apellidos'] || ''
        const celular = String(fila['Celular'] ?? '')
        const estado = fila['Estado'] || 'activo'

        if (!numeroDocumento) {
          skipped++
          const motivo = 'Sin número de documento (la contraseña inicial es el documento)'
          skippedAprendices.push({
            'Número de Documento': '',
            'Correo Electrónico': email || '',
            'Nombre': nombres,
            'Apellidos': apellidos,
            motivo,
          })
          processed.push({
            'Número de Documento': '',
            'Correo Electrónico': email || '',
            'Nombre': nombres,
            'Apellidos': apellidos,
            status: 'skipped',
            motivo,
          })
          continue
        }

        // Buscar existente en la base
        const existe = await Aprendiz.query()
          .useTransaction(trx)
          .where((q) => {
            if (numeroDocumento) q.where('numero_documento', numeroDocumento)
            if (email) q.orWhere('email', email)
          })
          .first()

        if (existe) {
          if (updateIfExists) {
            existe.merge({
              nombres: nombres || existe.nombres,
              apellidos: apellidos || existe.apellidos,
              celular: celular || existe.celular,
              estado: estado || existe.estado,
              tipo_documento: tipoDocumento || existe.tipo_documento,
              numero_documento: numeroDocumento || existe.numero_documento,
              email: email || existe.email,
              idgrupo: grupo.idgrupo || existe.idgrupo,
              idprograma_formacion: programa.idprograma_formacion || existe.idprograma_formacion,
              centro_formacion_idcentro_formacion:
                centroFormacionId || existe.centro_formacion_idcentro_formacion,
            })
            await existe.useTransaction(trx).save()
            updated++
            // registrar en processed como updated
            processed.push({
              'Número de Documento': numeroDocumento || '',
              'Correo Electrónico': email || '',
              'Nombre': nombres || '',
              'Apellidos': apellidos || '',
              'status': 'updated',
              'motivo': 'Actualizado',
            })
            // NO empujamos a skippedAprendices: fue una actualización
          } else {
            // NO actualizar, cuenta como omitido
            skipped++
            const motivo = 'Ya está en la base de datos'
            skippedAprendices.push({
              'Número de Documento': numeroDocumento || '',
              'Correo Electrónico': email || '',
              'Nombre': fila['Nombre'] || '',
              'Apellidos': fila['Apellidos'] || '',
              'motivo': motivo,
            })
            processed.push({
              'Número de Documento': numeroDocumento || '',
              'Correo Electrónico': email || '',
              'Nombre': nombres || '',
              'Apellidos': apellidos || '',
              'status': 'skipped',
              motivo,
            })
          }
        } else {
          // Clave inicial = número de documento. Si se olvida, recuperar-password.
          const hashedPassword = await bcrypt.hash(numeroDocumento, 10)
          const aprendizNuevo: any = {
            idgrupo: grupo.idgrupo,
            idprograma_formacion: programa.idprograma_formacion,
            perfil_idperfil: perfil.idperfil,
            nombres,
            apellidos,
            celular,
            estado,
            tipo_documento: tipoDocumento,
            numero_documento: numeroDocumento,
            email,
            password: hashedPassword,
            centro_formacion_idcentro_formacion: centroFormacionId,
          }
          const model = new Aprendiz()
          model.merge(aprendizNuevo)
          await model.useTransaction(trx).save()
          inserted++
          processed.push({
            'Número de Documento': numeroDocumento || '',
            'Correo Electrónico': email || '',
            'Nombre': nombres || '',
            'Apellidos': apellidos || '',
            'status': 'inserted',
            'motivo': 'Insertado',
          })
        }
      }

      await trx.commit()
      return response.ok({
        success: true,
        message: 'Importación procesada',
        inserted,
        updated,
        skipped,
        ficha: numeroGrupo,
        programa: nombrePrograma,
        centroFormacionId,
        skippedAprendices,
        processed,
      })
    } catch (error: any) {
      await trx.rollback()
      console.error('Error en importarAprendices:', error)
      return response
        .status(500)
        .json({ success: false, message: 'Error al importar aprendices', error: error.message })
    }
  }
}
