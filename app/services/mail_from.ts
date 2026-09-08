import env from '#start/env'

/**
 * Remitente para OTP y recuperación.
 * Con Gmail SMTP el "from" debe coincidir con SMTP_USERNAME.
 */
export function remitenteCorreo(): { address: string; name: string } {
  const name = env.get('SMTP_FROM_NAME') || 'SIGEVA'
  const address = (
    env.get('SMTP_FROM_EMAIL') ||
    env.get('SMTP_USERNAME') ||
    env.get('MAIL_FROM_ADDRESS') ||
    ''
  ).trim()

  return { address, name }
}
