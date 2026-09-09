import type { HttpContext } from '@adonisjs/core/http'
import type { NextFn } from '@adonisjs/core/types/http'
import Aprendiz from '#models/aprendiz'
import Usuario from '#models/usuario'
import { usuarioEstaActivo } from '#services/actor_sesion'
import {
  AUTH_COOKIE_NAME,
  diagnosticarJwt,
  esRutaPublica,
  leerToken,
  nombresCookies,
} from '#services/auth_jwt'

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

    if (method === 'OPTIONS' || esRutaPublica(method, pathname)) {
      return next()
    }

    const origin = ctx.request.header('origin') || '(sin origin)'
    const cookiesVistas = nombresCookies(ctx.request)
    const token = leerToken(ctx.request)

    if (!token) {
      console.error('[AUTH] 401 sin cookie/token', {
        method,
        pathname,
        origin,
        cookieHeader: Boolean(ctx.request.header('cookie')),
        cookiesVistas,
        cookieEsperada: AUTH_COOKIE_NAME,
        pista:
          cookiesVistas.length === 0
            ? 'El navegador no envió Cookie. Revisa withCredentials: true, CORS credentials y AUTH_COOKIE_SAMESITE (usa none+https si el front está en otro dominio).'
            : `Hay cookies (${cookiesVistas.join(', ')}) pero no ${AUTH_COOKIE_NAME}. El login no dejó la cookie o el dominio/path no coincide.`,
      })
      return ctx.response.status(401).json({
        success: false,
        message: 'No autenticado. Inicia sesión',
        motivo: 'sin_token',
      })
    }

    const diagnostico = diagnosticarJwt(token)
    if (!diagnostico.ok) {
      console.error('[AUTH] 401 JWT inválido o expirado', {
        method,
        pathname,
        origin,
        motivo: diagnostico.motivo,
        detalle: diagnostico.detalle,
        tokenLargo: token.length,
        tokenPreview: `${token.slice(0, 16)}...`,
      })
      return ctx.response.status(401).json({
        success: false,
        message: 'Sesión inválida o expirada.Inicia sesion de Nuevo ',
        motivo: diagnostico.motivo,
      })
    }

    const payload = diagnostico.payload

    if (payload.typ === 'usuario') {
      const usuario = await Usuario.query()
        .where('idusuarios', payload.sub)
        .preload('perfil')
        .first()
      if (!usuario || !usuarioEstaActivo(usuario.estado)) {
        console.error('[AUTH] 401 usuario inactivo o inexistente', {
          method,
          pathname,
          sub: payload.sub,
          existe: Boolean(usuario),
          estado: usuario?.estado,
        })
        return ctx.response.status(401).json({
          success: false,
          message: 'Tu usuario está inactivo o ya no existe',
          motivo: usuario ? 'usuario_inactivo' : 'usuario_inexistente',
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
        console.error('[AUTH] 401 aprendiz inexistente', {
          method,
          pathname,
          sub: payload.sub,
        })
        return ctx.response.status(401).json({
          success: false,
          message: 'Tu usuario está inactivo o ya no existe',
          motivo: 'aprendiz_inexistente',
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
