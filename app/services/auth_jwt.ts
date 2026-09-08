import { createHmac, timingSafeEqual } from 'node:crypto'
import type { HttpContext } from '@adonisjs/core/http'
import app from '@adonisjs/core/services/app'
import env from '#start/env'

export const AUTH_COOKIE_NAME = 'sigeva_token'

export type AuthTipo = 'usuario' | 'aprendiz'

export type AuthPayload = {
  sub: number
  typ: AuthTipo
  perfil: string
  iat: number
  exp: number
}

const RUTAS_PUBLICAS: Array<{ method: string; path: string }> = [
  { method: 'POST', path: '/api/usuarios/login' },
  { method: 'POST', path: '/api/aprendiz/login' },
  { method: 'POST', path: '/api/recuperar-password/solicitar' },
  { method: 'POST', path: '/api/recuperar-password/confirmar' },
  { method: 'POST', path: '/api/auth/logout' },
  { method: 'PUT', path: '/api/aprendiz/actualizar/contrasena' },
]

export function jwtTtlSeconds(): number {
  return env.get('JWT_EXPIRES_SECONDS') || 60 * 60 * 2
}

function secreto(): string {
  return env.get('APP_KEY')
}

function b64url(value: string | Buffer): string {
  return Buffer.from(value).toString('base64url')
}

function firmarHs256(data: string): string {
  return createHmac('sha256', secreto()).update(data).digest('base64url')
}

function firmasIguales(a: string, b: string): boolean {
  const left = Buffer.from(a)
  const right = Buffer.from(b)
  if (left.length !== right.length) return false
  return timingSafeEqual(left, right)
}

export function firmarJwt(claims: { sub: number; typ: AuthTipo; perfil: string }): string {
  const now = Math.floor(Date.now() / 1000)
  const header = b64url(JSON.stringify({ alg: 'HS256', typ: 'JWT' }))
  const payload = b64url(
    JSON.stringify({
      sub: claims.sub,
      typ: claims.typ,
      perfil: claims.perfil,
      iat: now,
      exp: now + jwtTtlSeconds(),
    } satisfies AuthPayload)
  )
  const data = `${header}.${payload}`
  return `${data}.${firmarHs256(data)}`
}

export function verificarJwt(token: string): AuthPayload | null {
  const parts = token.split('.')
  if (parts.length !== 3) return null

  const [header, payload, signature] = parts
  if (!firmasIguales(signature, firmarHs256(`${header}.${payload}`))) return null

  try {
    const parsed = JSON.parse(Buffer.from(payload, 'base64url').toString('utf8')) as AuthPayload
    if (!parsed || (parsed.typ !== 'usuario' && parsed.typ !== 'aprendiz')) return null
    if (!Number.isInteger(parsed.sub) || parsed.sub <= 0) return null
    if (parsed.exp < Math.floor(Date.now() / 1000)) return null
    return parsed
  } catch {
    return null
  }
}

export function opcionesCookieAuth() {
  const sameSite = env.get('AUTH_COOKIE_SAMESITE') || 'lax'
  return {
    httpOnly: true,
    secure: sameSite === 'none' ? true : app.inProduction,
    sameSite,
    maxAge: jwtTtlSeconds(),
    path: '/',
    encode: false as const,
  }
}

export function emitirCookieAuth(
  response: HttpContext['response'],
  claims: { sub: number; typ: AuthTipo; perfil: string }
) {
  const token = firmarJwt(claims)
  response.plainCookie(AUTH_COOKIE_NAME, token, opcionesCookieAuth())
  return token
}

export function limpiarCookieAuth(response: HttpContext['response']) {
  response.clearCookie(AUTH_COOKIE_NAME, { path: '/' })
}

export function leerToken(request: HttpContext['request']): string | null {
  const fromCookie = request.plainCookie(AUTH_COOKIE_NAME, { encoded: false })
  if (typeof fromCookie === 'string' && fromCookie.length > 0) return fromCookie

  const encoded = request.plainCookie(AUTH_COOKIE_NAME)
  if (typeof encoded === 'string' && encoded.length > 0) return encoded

  return null
}

export function leerSesion(request: HttpContext['request']): AuthPayload | null {
  const token = leerToken(request)
  if (!token) return null
  return verificarJwt(token)
}

export function idAprendizDeLaPeticion(request: HttpContext['request']): number | null {
  const sesion = leerSesion(request)
  return sesion?.typ === 'aprendiz' ? sesion.sub : null
}

export function esRutaPublica(method: string, pathname: string): boolean {
  const path = pathname.replace(/\/+$/, '') || '/'
  if (path === '/docs' || path.startsWith('/docs-')) return true
  return RUTAS_PUBLICAS.some((ruta) => ruta.method === method.toUpperCase() && ruta.path === path)
}
