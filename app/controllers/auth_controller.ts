import type { HttpContext } from '@adonisjs/core/http'
import Aprendiz from '#models/aprendiz'
import Usuario from '#models/usuario'
import { actorDesdeUsuario, usuarioEstaActivo } from '#services/actor_sesion'
import { leerSesion, limpiarCookieAuth } from '#services/auth_jwt'

export default class AuthController {
  async me({ request, response }: HttpContext) {
    const sesion = leerSesion(request)
    if (!sesion) {
      return response.status(401).json({
        success: false,
        message: 'No autenticado. Inicia sesión',
      })
    }

    if (sesion.typ === 'usuario') {
      const usuario = await Usuario.query().where('idusuarios', sesion.sub).preload('perfil').first()
      if (!usuario || !usuarioEstaActivo(usuario.estado)) {
        return response.status(401).json({
          success: false,
          message: 'Tu usuario está inactivo o ya no existe',
        })
      }

      const actor = actorDesdeUsuario(usuario)
      return response.ok({
        success: true,
        data: {
          tipo: 'usuario',
          id: usuario.idusuarios,
          email: usuario.email,
          nombres: usuario.nombres,
          apellidos: usuario.apellidos,
          estado: usuario.estado,
          perfil: actor.perfil,
          centroFormacion: actor.idcentro,
        },
      })
    }

    const aprendiz = await Aprendiz.query()
      .where('idaprendiz', sesion.sub)
      .preload('perfil')
      .preload('grupo')
      .preload('programa')
      .first()

    if (!aprendiz) {
      return response.status(401).json({
        success: false,
        message: 'Tu usuario está inactivo o ya no existe',
      })
    }

    return response.ok({
      success: true,
      data: {
        tipo: 'aprendiz',
        id: aprendiz.idaprendiz,
        email: aprendiz.email,
        nombres: aprendiz.nombres,
        apellidos: aprendiz.apellidos,
        estado: aprendiz.estado,
        perfil: aprendiz.perfil?.perfil ?? 'Aprendiz',
        jornada: aprendiz.grupo?.jornada || null,
        programa: aprendiz.programa?.programa || null,
        CentroFormacion: aprendiz.centro_formacion_idcentro_formacion,
      },
    })
  }

  async logout({ response }: HttpContext) {
    limpiarCookieAuth(response)
    return response.ok({
      success: true,
      message: 'Sesión cerrada',
    })
  }
}
