// import type { HttpContext } from '@adonisjs/core/http'

import Aprendiz from '#models/aprendiz'
import { HttpContext } from '@adonisjs/core/http'
import Grupo from '#models/grupo'
import ProgramaFormacion from '#models/programa_formacion'
import NivelFormacion from '#models/nivel_formacion'
import db from '@adonisjs/lucid/services/db'
import Perfil from '#models/perfil'
import {
  bloquearSiCentroAjeno,
  resolverActor,
} from '#services/actor_sesion'
import { emitirCookieAuth } from '#services/auth_jwt'

//contraseña
import bcrypt from 'bcrypt'

export default class AprendizsController {
  async registro({ request, response }: HttpContext) {
    const trx = await db.transaction()

    try {
      const data = request.only([
        'grupo',
        'jornada',
        'programa',
        'codigo_programa',
        'version',
        'duracion',
        'idnivel_formacion',
        'idarea_tematica',
        'perfil_idperfil',
        'nombres',
        'apellidos',
        'celular',
        'estado',
        'tipo_documento',
        'numero_documento',
        'email',
        'password',
        'nivel_formacion',
        'centro_formacion_idcentro_formacion',
      ])

      const actor = await resolverActor(request)
      if (bloquearSiCentroAjeno(actor, data.centro_formacion_idcentro_formacion, response)) {
        await trx.rollback()
        return
      }
      if (actor?.esDeCentro) {
        data.centro_formacion_idcentro_formacion = actor.idcentro
      }

      // Verificar si el email ya existe
      const emailExist = await Aprendiz.findBy('email', data.email)
      if (emailExist) {
        await trx.rollback()
        return response.status(400).json({
          message: 'El correo ya está registrado',
        })
      }

      // Buscar o crear grupo
      let grupo = await Grupo.query({ client: trx }).where('grupo', data.grupo).first()
      if (!grupo) {
        grupo = await Grupo.create({ grupo: data.grupo, jornada: data.jornada }, { client: trx })
      }

      // Buscar o crear nivel
      let nivel = await NivelFormacion.query({ client: trx })
        .where('idnivel_formacion', data.idnivel_formacion)
        .first()

      if (!nivel) {
        nivel = await NivelFormacion.create(
          {
            idnivel_formacion: data.idnivel_formacion,
            nivel_formacion: data.nivel_formacion,
          },
          { client: trx }
        )
      }

      // Buscar o crear programa
      let programa = await ProgramaFormacion.query({ client: trx })
        .where('codigo_programa', data.codigo_programa)
        .first()

      if (!programa) {
        programa = await ProgramaFormacion.create(
          {
            programa: data.programa,
            codigo_programa: data.codigo_programa,
            version: data.version,
            duracion: data.duracion,
            idnivel_formacion: nivel.idnivel_formacion,
            idarea_tematica: data.idarea_tematica,
          },
          { client: trx }
        )
      }

      // Hashear contraseña
      const hashedPassword = await bcrypt.hash(data.password, 10)
      const perfilaprendiz = await Perfil.query({ client: trx })
        .where('perfil', 'Aprendiz') // errorsito corregido
        .first()
      if (!perfilaprendiz) {
        await trx.rollback()
        return response.status(500).json({
          message: 'El perfil "Aprendiz" no existe, Debes crearlo antes en la base de datos',
        })
      }

      // Crear aprendiz solo con sus campos
      const aprendiz = await Aprendiz.create(
        {
          perfil_idperfil: perfilaprendiz.idperfil,

          nombres: data.nombres,
          apellidos: data.apellidos,
          celular: data.celular,
          estado: data.estado,
          tipo_documento: data.tipo_documento,
          numero_documento: data.numero_documento,
          email: data.email,
          password: hashedPassword,
          idgrupo: grupo.idgrupo,
          idprograma_formacion: programa.idprograma_formacion,
          centro_formacion_idcentro_formacion: data.centro_formacion_idcentro_formacion,
        },
        { client: trx }
      )

      await trx.commit()

      return response.created({
        message: 'Aprendiz creado con éxito',
        data: aprendiz,
      })
    } catch (error) {
      await trx.rollback()
      console.error(error)
      return response.status(500).json({
        message: 'Error al registrar aprendiz',
        error: error.message,
      })
    }
  }

  async traer({ request, response }: HttpContext) {
    try {
      const actor = await resolverActor(request)
      if (actor?.esDeCentro && !actor.idcentro) {
        return response.status(400).json({
          message: 'Tu usuario no tiene centro de formación asignado',
        })
      }

      const query = Aprendiz.query()
        .preload('centro_formacion', (cf) => {
          cf.preload('regional')
        })
        .preload('programa', (p) => p.select(['idprograma_formacion', 'programa']))
        .preload('grupo', (g) => g.select(['idgrupo', 'grupo', 'jornada']))

      if (actor?.esDeCentro && actor.idcentro) {
        query.where('centro_formacion_idcentro_formacion', actor.idcentro)
      }

      const aprendices = await query
        .orderBy('centro_formacion_idcentro_formacion', 'asc')
        .orderBy('apellidos', 'asc')
      return response.ok(aprendices)
    } catch (error) {
      return response.status(500).send({
        message: 'Error al obtener aprendices',
        error: error.message
      })
    }
  }

  async actualizar({ request, response, params }: HttpContext) {
    try {
      const id = params.id
      const aprendiz = await Aprendiz.find(id)

      if (!aprendiz) {
        return response.status(404).json({ message: 'Aprendiz no encontrado' })
      }

      const actor = await resolverActor(request)
      if (bloquearSiCentroAjeno(actor, aprendiz.centro_formacion_idcentro_formacion, response)) {
        return
      }

      const data = request.only([
        'idgrupo',
        'idprograma_formacion',
        'perfil_idperfil',
        'nombres',
        'apellidos',
        'celular',
        'estado',
        'tipo_documento',
        'numero_documento',
        'email',
        'password',
      ])

      // Verificar email si se cambió
      if (data.email && data.email !== aprendiz.email) {
        const emailExist = await Aprendiz.findBy('email', data.email)
        if (emailExist) {
          return response.status(400).json({
            message: 'El correo ya está registrado, por favor usa otro',
          })
        }
      }

      // Hash de contraseña solo si se proporciona
      if (data.password) {
        data.password = await bcrypt.hash(data.password, 10)
      }

      aprendiz.merge(data)
      await aprendiz.save()

      return response.ok({
        message: 'Aprendiz actualizado con éxito',
        data: aprendiz,
      })
    } catch (error) {
      return response.status(500).json({
        message: 'Error al actualizar aprendiz',
        error: error.message,
      })
    }
  }

  async actualizarContrasena({ response }: HttpContext) {
    return response.status(410).json({
      success: false,
      message:
        'Este endpoint ya no está disponible. Usa POST /api/recuperar-password/solicitar y POST /api/recuperar-password/confirmar',
    })
  }

  async login({ request, response }: HttpContext) {
    try {
      const { email, password } = request.only(['email', 'password'])

      const aprendizExist = await Aprendiz.query()
        .where('email', email)
        .preload('perfil')
        .preload('grupo')
        .preload('programa')
        .first()

      if (!aprendizExist)
        return response.status(401).json({ success: false, message: 'Fallo en la autenticación' })

      const verifyPassword = await bcrypt.compare(password, aprendizExist.password)

      if (!verifyPassword)
        return response.status(401).json({ success: false, message: 'Fallo en la autenticación' })

      emitirCookieAuth(response, {
        sub: aprendizExist.idaprendiz,
        typ: 'aprendiz',
        perfil: aprendizExist.perfil?.perfil ?? 'Aprendiz',
      })

      return response.status(200).json({
        success: true,
        message: 'Autenticado',
        data: {
          id: aprendizExist.idaprendiz,
          nombre: aprendizExist.nombres,
          apellidos: aprendizExist.apellidos,
          estado: aprendizExist.estado,
          perfil: aprendizExist.perfil.perfil,
          jornada: aprendizExist.grupo?.jornada || null,
          programa: aprendizExist.programa?.programa || null,
          CentroFormacion: aprendizExist.centro_formacion_idcentro_formacion,
        },
      })
    } catch (e) {
      return response.status(500).json({ message: 'Error', error: e.message })
    }
  }
  async aprendicesPorCentro({ params, request, response }: HttpContext) {
    try {
      const idCentro = Number(params.idCentro)
      const actor = await resolverActor(request)
      if (bloquearSiCentroAjeno(actor, idCentro, response)) return

      const { page = 1, perPage = 20, estado, search } = request.qs()

      const query = Aprendiz.query()
        .where('centro_formacion_idcentro_formacion', idCentro)
        .preload('grupo')
        .preload('programa')
        .preload('perfil')
        .preload('centro_formacion', (cf) => cf.select(['centro_formacioncol']))

      if (estado) {
        query.where('estado', estado)
      }

      if (search) {
        query.where((builder) => {
          builder
            .whereILike('nombres', `%${search}%`)
            .orWhereILike('apellidos', `%${search}%`)
            .orWhereILike('email', `%${search}%`)
            .orWhere('numero_documento', search)
        })
      }

      const result = await query.orderBy('apellidos', 'asc').paginate(Number(page), Number(perPage))
      const { data } = result.toJSON()
      return response.ok(data)
    } catch (error) {
      console.error('Error al traer aprendices por centro:', error)
      return response.status(500).json({
        message: 'Error al traer aprendices por centro de formación',
        error: error.message,
      })
    }
  }
  async aprendicesAvaibleAll({ request, response }: HttpContext) {
    try {
      const actor = await resolverActor(request)
      if (actor?.esDeCentro && !actor.idcentro) {
        return response.status(400).json({
          message: 'Tu usuario no tiene centro de formación asignado',
        })
      }

      const query = Aprendiz.query().whereRaw('LOWER(estado) IN (?, ?)', [
        'en formacion',
        'activo',
      ])
      if (actor?.esDeCentro && actor.idcentro) {
        query.where('centro_formacion_idcentro_formacion', actor.idcentro)
      }

      const aprendices = await query
      return response.status(200).json({
        message: 'Éxito',
        data: aprendices,
      })
    } catch (e) {
      return response.status(500).json({ message: 'Error', error: e.message })
    }
  }
  async aprendicesAvailableByCentros({ params, request, response }: HttpContext) {
    try {
      const { id } = params
      const actor = await resolverActor(request)
      if (bloquearSiCentroAjeno(actor, id, response)) return

      const aprendices = await Aprendiz.query()
        .where('centro_formacion_idcentro_formacion', id)
        .whereRaw('LOWER(estado) IN (?, ?)', ['en formacion', 'activo'])
      return response.status(200).json({
        message: 'Éxito',
        data: aprendices,
      })
    } catch (e) {
      return response.status(500).json({
        message: 'Error al obtener los aprendices',
        error: e.message,
      })
    }
  }
  async aprendicesInscritosByCentro({ params, request, response }: HttpContext) {
    try {
      const { id } = params
      const actor = await resolverActor(request)
      if (bloquearSiCentroAjeno(actor, id, response)) return

      const aprendices = await Aprendiz.query()
        .where('centro_formacion_idcentro_formacion', id)
        .preload('grupo')
        .preload('programa')
        .preload('perfil')
        .preload('centro_formacion', (cf) => cf.select(['centro_formacioncol']))

      return response.status(200).json({
        message: 'Éxito',
        data: aprendices,
      })
    } catch (e) {
      return response.status(500).json({
        message: 'Error al obtener los aprendices',
        error: e.message,
      })
    }
  }
}
