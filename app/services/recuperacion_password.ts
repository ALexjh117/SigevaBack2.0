import Aprendiz from '#models/aprendiz'
import Usuario from '#models/usuario'
import { DateTime } from 'luxon'

export type TipoCuentaRecuperable = 'usuario' | 'aprendiz'

export type CuentaRecuperable = {
  tipo: TipoCuentaRecuperable
  id: number
  email: string
  nombres: string
  apellidos: string
  perfil: string
}

export function normalizarEmail(email: string) {
  return email.trim().toLowerCase()
}

export function minutosExpiracionOtp() {
  const parsed = parseInt(process.env.OTP_EXPIRATION_MINUTES || '5', 10)
  return Number.isFinite(parsed) && parsed > 0 ? parsed : 5
}

export function otpExpirado(creadoEn: DateTime, ahora = DateTime.now()) {
  return ahora > creadoEn.plus({ minutes: minutosExpiracionOtp() })
}

/**
 * Busca la cuenta por correo en usuarios (staff) y, si no aparece, en aprendiz.
 * El mismo endpoint sirve para Administrador, admin_sistema, Funcionario y Aprendiz.
 */
export async function buscarCuentaPorEmail(email: string): Promise<CuentaRecuperable | null> {
  const emailNorm = normalizarEmail(email)

  const usuario = await Usuario.query()
    .whereRaw('LOWER(TRIM(email)) = ?', [emailNorm])
    .preload('perfil')
    .first()

  if (usuario) {
    return {
      tipo: 'usuario',
      id: usuario.idusuarios,
      email: usuario.email.trim(),
      nombres: usuario.nombres,
      apellidos: usuario.apellidos,
      perfil: usuario.perfil?.perfil || String(usuario.idperfil),
    }
  }

  const aprendiz = await Aprendiz.query()
    .whereRaw('LOWER(TRIM(email)) = ?', [emailNorm])
    .preload('perfil')
    .first()

  if (aprendiz) {
    return {
      tipo: 'aprendiz',
      id: aprendiz.idaprendiz,
      email: aprendiz.email.trim(),
      nombres: aprendiz.nombres,
      apellidos: aprendiz.apellidos,
      perfil: aprendiz.perfil?.perfil || 'Aprendiz',
    }
  }

  return null
}
