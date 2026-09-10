import { defineConfig } from '@adonisjs/cors'
import env from '#start/env'

/**
 * Configuration options to tweak the CORS policy. The following
 * options are documented on the official documentation website.
 *
 * https://docs.adonisjs.com/guides/security/cors
 */
const isProduction = env.get('NODE_ENV') === 'production'

const corsConfig = defineConfig({
  enabled: true,
  origin: isProduction
    ? ['https://sigevafront2-0.onrender.com', 'https://sigeva.cloudsenactpi.net']
    : ['https://sigevafront2-0.onrender.com', 'https://sigeva.cloudsenactpi.net', 'http://localhost:5173', 'http://localhost:3000', 'http://127.0.0.1:5173', 'http://127.0.0.1:3000'],
  methods: ['GET', 'HEAD', 'POST', 'PUT', 'PATCH', 'DELETE', 'OPTIONS'],
  headers: true,
  exposeHeaders: [],
  credentials: true,
  maxAge: 90,
})

export default corsConfig
