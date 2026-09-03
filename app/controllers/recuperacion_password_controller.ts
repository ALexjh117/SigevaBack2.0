import type { HttpContext } from '@adonisjs/core/http'
import vine from '@vinejs/vine'
import { nanoid } from 'nanoid'
import bcrypt from 'bcrypt'
import mail from '@adonisjs/mail/services/main'
import RecuperacionPassword from '#models/recuperacion_password'
import Aprendiz from '#models/aprendiz'
import Usuario from '#models/usuario'
import {
  buscarCuentaPorEmail,
  minutosExpiracionOtp,
  normalizarEmail,
  otpExpirado,
} from '#services/recuperacion_password'

export default class RecuperacionPasswordController {
  /**
   * POST /api/recuperar-password/solicitar
   * Genera un OTP de 6 caracteres y lo envía al correo. Sirve para los 4 roles.
   */
  async solicitar({ request, response }: HttpContext) {
    try {
      const validator = vine.compile(
        vine.object({
          email: vine.string().trim().email(),
        })
      )
      const data = await request.validateUsing(validator)
      const emailNorm = normalizarEmail(data.email)

      const cuenta = await buscarCuentaPorEmail(emailNorm)
      if (!cuenta) {
        return response.status(404).json({
          success: false,
          message: 'No hay una cuenta con ese correo',
          codigo_error: 'CUENTA_NO_ENCONTRADA',
        })
      }

      await RecuperacionPassword.query()
        .where('email', emailNorm)
        .where('codigo', 'not like', 'USED_%')
        .delete()

      const otpCode = nanoid(6).toUpperCase()
      const expirationMinutes = minutosExpiracionOtp()

      await RecuperacionPassword.create({
        email: emailNorm,
        codigo: otpCode,
        tipo: cuenta.tipo,
        idReferencia: cuenta.id,
      })

      let emailEnviado = false
      try {
        await mail.send((message) => {
          message
            .to(cuenta.email)
            .from(process.env.MAIL_FROM_ADDRESS || 'noreply@sigeva.com')
            .subject('Código para recuperar tu contraseña - SIGEVA').html(`
              <h2>Recuperar contraseña</h2>
              <p>Hola ${cuenta.nombres} ${cuenta.apellidos},</p>
              <p>Tu código para cambiar la contraseña es:
                <strong style="font-size: 24px; color: #007bff;">${otpCode}</strong>
              </p>
              <p>Este código expira en ${expirationMinutes} minutos.</p>
              <p>Si no pediste este cambio, ignora este correo.</p>
            `)
        })
        emailEnviado = true
      } catch (emailError) {
        console.error('❌ Error enviando email de recuperación:', {
          error: emailError.message,
          code: emailError.code,
        })
      }

      if (!emailEnviado && process.env.NODE_ENV === 'production') {
        return response.status(500).json({
          success: false,
          message: 'No se pudo enviar el correo. Intenta de nuevo más tarde.',
          codigo_error: 'EMAIL_NO_ENVIADO',
        })
      }

      return response.status(200).json({
        success: true,
        message: 'Código enviado al correo',
        data: {
          otp_generado: true,
          email_enviado_a: cuenta.email,
          email_enviado: emailEnviado,
          expira_en_minutos: expirationMinutes,
        },
      })
    } catch (error) {
      if (error.messages) {
        return response.status(400).json({
          success: false,
          message: 'Datos de entrada inválidos',
          errors: error.messages,
        })
      }
      return response.status(500).json({
        success: false,
        message: 'Error al solicitar el código',
        error: error.message,
      })
    }
  }

  /**
   * POST /api/recuperar-password/confirmar
   * Valida el OTP y guarda la nueva contraseña (bcrypt) en usuarios o aprendiz.
   */
  async confirmar({ request, response }: HttpContext) {
    try {
      const validator = vine.compile(
        vine.object({
          email: vine.string().trim().email(),
          codigo: vine.string().trim().minLength(6).maxLength(6),
          nueva_password: vine.string().minLength(8).maxLength(72),
        })
      )
      const data = await request.validateUsing(validator)
      const emailNorm = normalizarEmail(data.email)
      const codigo = data.codigo.toUpperCase()

      const registro = await RecuperacionPassword.query()
        .where('email', emailNorm)
        .where('codigo', codigo)
        .first()

      if (!registro) {
        return response.status(400).json({
          success: false,
          message: 'El código no es válido o ya fue usado',
          codigo_error: 'OTP_INVALIDO',
        })
      }

      if (otpExpirado(registro.createdAt)) {
        await registro.delete()
        return response.status(400).json({
          success: false,
          message: 'El código ya expiró. Solicita uno nuevo.',
          codigo_error: 'OTP_EXPIRADO',
        })
      }

      const hash = await bcrypt.hash(data.nueva_password, 10)
      let perfil = registro.tipo === 'aprendiz' ? 'Aprendiz' : 'usuario'

      if (registro.tipo === 'usuario') {
        const usuario = await Usuario.query()
          .where('idusuarios', registro.idReferencia)
          .preload('perfil')
          .first()
        if (!usuario) {
          return response.status(404).json({
            success: false,
            message: 'No hay una cuenta con ese correo',
            codigo_error: 'CUENTA_NO_ENCONTRADA',
          })
        }
        usuario.password = hash
        await usuario.save()
        perfil = usuario.perfil?.perfil || perfil
      } else {
        const aprendiz = await Aprendiz.find(registro.idReferencia)
        if (!aprendiz) {
          return response.status(404).json({
            success: false,
            message: 'No hay una cuenta con ese correo',
            codigo_error: 'CUENTA_NO_ENCONTRADA',
          })
        }
        aprendiz.password = hash
        await aprendiz.save()
      }

      await RecuperacionPassword.query().where('email', emailNorm).delete()

      return response.status(200).json({
        success: true,
        message: 'Contraseña actualizada con éxito',
        data: {
          perfil,
          login:
            registro.tipo === 'aprendiz' ? '/api/aprendiz/login' : '/api/usuarios/login',
        },
      })
    } catch (error) {
      if (error.messages) {
        return response.status(400).json({
          success: false,
          message: 'Datos de entrada inválidos',
          errors: error.messages,
        })
      }
      return response.status(500).json({
        success: false,
        message: 'Error al cambiar la contraseña',
        error: error.message,
      })
    }
  }
}
