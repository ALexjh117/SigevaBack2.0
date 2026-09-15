import type { HttpContext } from '@adonisjs/core/http'
import { storeCandidatoValidator } from '#validators/store_candidato_validator'
import CandidatosService from '#services/candidatos_service'
import {
  bloquearSiCentroAjeno,
  bloquearSiNoPuedeGestionarElecciones,
  resolverActor,
} from '#services/actor_sesion'
import Eleccione from '#models/eleccione'

export default class CandidatosController {
  public async store({ request, response }: HttpContext) {
    const actor = await resolverActor(request)
    if (bloquearSiNoPuedeGestionarElecciones(actor, response)) return

    const payload = await request.validateUsing(storeCandidatoValidator)

    const eleccion = await Eleccione.find(payload.ideleccion)
    if (!eleccion) {
      return response.badRequest({ message: 'La elección no existe' })
    }
    if (bloquearSiCentroAjeno(actor, eleccion.idcentro_formacion, response)) return

    const fotoFile = request.file('foto', {
      size: '5mb',
      extnames: ['jpg', 'jpeg', 'png', 'webp'],
    })

    try {
      const candidato = await CandidatosService.createWithOptionalUpload(
        {
          nombres: payload.nombres ?? 'Candidato',
          ideleccion: payload.ideleccion,
          idaprendiz: payload.idaprendiz,
          propuesta: payload.propuesta,
          numero_tarjeton: payload.numero_tarjeton,
          jornada: payload.jornada,
          foto_url: payload.foto_url ?? null,
        },
        fotoFile?.tmpPath ?? null
      )

      return response.created({
        message: 'Candidato registrado exitosamente',
        data: candidato,
      })
    } catch (error: any) {
      return response.badRequest({
        message: error?.message ?? 'Error al registrar candidato',
      })
    }
  }

  public async getbycentroformacion({ params, request, response }: HttpContext) {
    try {
      const actor = await resolverActor(request)
      const { idcentro_formacion } = params
      if (bloquearSiCentroAjeno(actor, idcentro_formacion, response)) return

      const candidatos = await CandidatosService.getCandidatoCentroFormacion(
        Number(idcentro_formacion)
      )
      return response.ok({
        message: 'Candidatos obtenidos correctamente',
        data: candidatos,
      })
    } catch (error: any) {
      return response.badRequest({
        message: error?.message ?? 'Error al obtener candidatos',
      })
    }
  }

  public async getByEleccion({ params, request, response }: HttpContext) {
    try {
      const ideleccion = Number(params.ideleccion)
      if (Number.isNaN(Number(ideleccion))) {
        return response.badRequest({
          message: 'El parámetro ideleccion debe ser un número válido',
        })
      }

      const actor = await resolverActor(request)
      const eleccion = await Eleccione.find(ideleccion)
      if (eleccion && bloquearSiCentroAjeno(actor, eleccion.idcentro_formacion, response)) return

      const { jornada } = request.qs()
      const candidatos = await CandidatosService.getAllCandidatosByIdEleccion(
        Number(ideleccion),
        typeof jornada === 'string' ? jornada : undefined
      )

      return response.ok({
        message: 'Candidatos obtenidos correctamente',
        data: candidatos,
      })
    } catch (error: any) {
      return response.badRequest({
        message: error?.message ?? 'Error al obtener candidatos',
      })
    }
  }

  public async update({ params, request, response }: HttpContext) {
    try {
      const actor = await resolverActor(request)
      if (bloquearSiNoPuedeGestionarElecciones(actor, response)) return

      const idcandidatos = Number(params.id)
      if (Number.isNaN(idcandidatos)) {
        return response.badRequest({ message: 'El parámetro id debe ser numérico' })
      }

      const fotoFile = request.file('foto', {
        size: '5mb',
        extnames: ['jpg', 'jpeg', 'png', 'webp'],
      })

      const data = request.only([
        'nombres',
        'ideleccion',
        'idaprendiz',
        'propuesta',
        'numero_tarjeton',
        'jornada',
        'foto_url',
      ])

      if (data.ideleccion) {
        const eleccion = await Eleccione.find(data.ideleccion)
        if (eleccion && bloquearSiCentroAjeno(actor, eleccion.idcentro_formacion, response)) return
      }

      const candidato = await CandidatosService.updateCandidatos(
        idcandidatos,
        data,
        fotoFile?.tmpPath ?? null
      )

      return response.ok({
        message: 'Candidato actualizado correctamente',
        data: candidato,
      })
    } catch (error: any) {
      return response.badRequest({
        message: error?.message ?? 'Error al actualizar candidato',
      })
    }
  }

  public async delete({ params, request, response }: HttpContext) {
    try {
      const actor = await resolverActor(request)
      if (bloquearSiNoPuedeGestionarElecciones(actor, response)) return

      const idcandidatos = Number(params.id)
      if (Number.isNaN(idcandidatos)) {
        return response.badRequest({ message: 'El parámetro id debe ser numérico' })
      }

      const result = await CandidatosService.deleteCandidato(idcandidatos)
      return response.ok(result)
    } catch (error: any) {
      return response.badRequest({
        message: error?.message ?? 'Error al eliminar candidato',
      })
    }
  }

  public async show({ response }: HttpContext) {
    try {
      const candidatos = await CandidatosService.getAllCandidatos()

      return response.ok({
        message: 'Candidatos obtenidos correctamente',
        data: candidatos,
      })
    } catch (error: any) {
      return response.badRequest({
        message: error?.message ?? 'Error al obtener candidatos',
      })
    }
  }
}
