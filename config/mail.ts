import { defineConfig, transports } from '@adonisjs/mail'
import env from '#start/env'
import { remitenteCorreo } from '#services/mail_from'

const remitente = remitenteCorreo()

const mailConfig = defineConfig({
  default: env.get('MAIL_MAILER') || 'smtp',

  from: {
    address: remitente.address,
    name: remitente.name,
  },

  mailers: {
    smtp: transports.smtp({
      host: env.get('SMTP_HOST') || 'smtp.gmail.com',
      port: env.get('SMTP_PORT') || 587,
      secure: env.get('SMTP_SECURE') ?? false,
      auth: {
        type: 'login',
        user: env.get('SMTP_USERNAME') || '',
        pass: (env.get('SMTP_PASSWORD') || '').replace(/\s/g, ''),
      },
    }),
    resend: transports.resend({
      baseUrl: 'https://api.resend.com',
      key: env.get('RESEND_API_KEY') || '',
    }),
  },
})

export default mailConfig

declare module '@adonisjs/mail/types' {
  export interface MailersList extends InferMailers<typeof mailConfig> {}
}
