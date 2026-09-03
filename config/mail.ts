import { defineConfig, transports } from '@adonisjs/mail'
import env from '#start/env'

const mailConfig = defineConfig({
  default: 'resend',

  mailers: {
    resend: transports.resend({
        baseUrl: 'https://api.resend.com',
      key: env.get('RESEND_API_KEY'),
    }),
  },
})

export default mailConfig

declare module '@adonisjs/mail/types' {
  export interface MailersList extends InferMailers<typeof mailConfig> {}
}

















