import type { HttpContext } from '@adonisjs/core/http'
import type { NextFn } from '@adonisjs/core/types/http'
import Aprendiz from '#models/aprendiz'
import Usuario from '#models/usuario'
import { esRutaPublica, leerToken, verificarJwt } from '#services/auth_jwt'

declare module '@adonisjs/core/http' {
  interface HttpContext {
    authSesion?: {
      sub: number
      typ: 'usuario' | 'aprendiz'
      perfil: string
    }
  }
}

export default class AuthMiddleware {
  async handle(ctx: HttpContext, next: NextFn) {
    const method = ctx.request.method()
    const pathname = ctx.request.url().split('?')[0]

    if (esRutaPublica(method, pathname)) {
      return next()
    }

    const token = leerToken(ctx.request)
    if (!token) {
      return ctx.response.status(401).json({
        success: false,
        message: 'No autenticado. Inicia sesión',
      })
    }

    const payload = verificarJwt(token)
    if (!payload) {
      return ctx.response.status(401).json({
        success: false,
        message: 'Sesión inválida o expirada.Inicia sesion de Nuevo ',
      })
    }

    if (payload.typ === 'usuario') {
      const usuario = await Usuario.query()
        .where('idusuarios', payload.sub)
        .preload('perfil')
        .first()
      if (!usuario || String(usuario.estado).toLowerCase() !== 'activo ') {
        return ctx.response.status(401).json({
          success: false,
          message: 'Tu usuario está inactivo o ya no existe',
        })
      }
      ctx.authSesion = {
        sub: usuario.idusuarios,
        typ: 'usuario',
        perfil: usuario.perfil?.perfil ?? payload.perfil,
      }
    } else {
      const aprendiz = await Aprendiz.query()
        .where('idaprendiz', payload.sub)
        .preload('perfil')
        .first()
      if (!aprendiz) {
        return ctx.response.status(401).json({
          success: false,
          message: 'Tu usuario está inactivo o ya no existe',
        })
      }
      ctx.authSesion = {
        sub: aprendiz.idaprendiz,
        typ: 'aprendiz',
        perfil: aprendiz.perfil?.perfil ?? 'Aprendiz',
      }
    }

    return next()
  }
}
