import type { HttpContext } from '@adonisjs/core/http'
import ValidacionVoto from '#models/validacion_voto'
import vine from '@vinejs/vine'
import { nanoid } from 'nanoid'
import { DateTime } from 'luxon'
import mail from '@adonisjs/mail/services/main'

export default class ValidacionVotoController {
  /**
   * Obtener todas las validaciones de voto
   */
  async index({ response }: HttpContext) {
    try {
      const validaciones = await ValidacionVoto.query()
        .preload('aprendiz')
        .preload('eleccion')
        .orderBy('id', 'desc')

      return response.status(200).json({
        message: 'Validaciones obtenidas exitosamente',
        data: validaciones,
      })
    } catch (error) {
      return response.status(500).json({
        message: 'Error al obtener las validaciones',
        error: error.message,
      })
    }
  }
  /**
   * Obtener una validación específica
   */
  async show({ params, response }: HttpContext) {
    try {
      const validacion = await ValidacionVoto.query()
        .where('id', params.id)
        .preload('aprendiz')
        .preload('eleccion')
        .first()

      if (!validacion) {
        return response.status(404).json({
          message: 'Validación no encontrada',
        })
      }

      return response.status(200).json({
        message: 'Validación obtenida exitosamente',
        data: validacion,
      })
    } catch (error) {
      return response.status(500).json({
        message: 'Error al obtener la validación',
        error: error.message,
      })
    }
  }

  /**
   * Generar OTP para votación
   * Endpoint: POST /api/validaciones/generar-otp
   */
  async generarOtp({ request, response }: HttpContext) {
    try {
      // Validación de datos de entrada
      const validator = vine.compile(
        vine.object({
          aprendiz_idaprendiz: vine.number().positive(),
          elecciones_ideleccion: vine.number().positive(),
        })
      )

      const data = await request.validateUsing(validator)

      // 1. Verificar que el aprendiz existe y está activo
      const aprendiz = await (await import('#models/aprendiz')).default
        .query()
        .where('idaprendiz', data.aprendiz_idaprendiz)
        .preload('centro_formacion')
        .first()

      if (!aprendiz) {
        return response.status(404).json({
          message: 'El aprendiz especificado no existe',
          codigo_error: 'APRENDIZ_NO_ENCONTRADO',
        })
      }

      const estadosPermitidos = [
        'activo',
        'en formacion',
        'suspension',
        'pendiente',
        'condicionado',
      ]

      // Normalizar estado del aprendiz a minúsculas y eliminar espacios
      const estadoAprendiz = (aprendiz.estado || '').toString().trim().toLowerCase()

      if (!estadosPermitidos.includes(estadoAprendiz)) {
        return response.status(400).json({
          message: `El aprendiz debe estar en uno de los estados permitidos: ${estadosPermitidos.join(', ')}`,
          codigo_error: 'APRENDIZ_ESTADO_INVALIDO',
        })
      }
      // 2. Verificar que la elección existe y está activa
      const eleccion = await (await import('#models/eleccione')).default
        .query()
        .where('ideleccion', data.elecciones_ideleccion)
        .preload('centro')
        .first()

      if (!eleccion) {
        return response.status(404).json({
          message: 'La elección especificada no existe',
          codigo_error: 'ELECCION_NO_ENCONTRADA',
        })
      }
     


      // 3. Verificar fechas de la elección
    // --- Preparación de datos ---
    // const hoy = DateTime.now().setZone("America/Bogota")
    // const soloFechaHoy = hoy.toISODate() ?? ""

    // const fechaInicio = new Date(eleccion.fecha_inicio)
    // const fechaFin = new Date(eleccion.fecha_fin)
    // const soloFechaInicio = fechaInicio.toISOString().split("T")[0]
    // const soloFechaFin = fechaFin.toISOString().split("T")[0]

    // const horaInicioDate = new Date(eleccion.hora_inicio as any)
    // const horaFinDate = new Date(eleccion.hora_fin as any)

    // const minutosInicio = horaInicioDate.getHours() * 60 + horaInicioDate.getMinutes()
    // const minutosFin = horaFinDate.getHours() * 60 + horaFinDate.getMinutes()
    // const minutosAhora = hoy.hour * 60 + hoy.minute

    // // --- Validación ---
    // const esValida =
    //   // Caso 1: hoy está entre fechaInicio y fechaFin (días intermedios)
    //   (soloFechaHoy > soloFechaInicio && soloFechaHoy < soloFechaFin) ||

    //   // Caso 2: rango dentro del mismo día
    //   (soloFechaHoy === soloFechaInicio &&
    //     soloFechaHoy === soloFechaFin &&
    //     minutosAhora >= minutosInicio &&
    //     minutosAhora <= minutosFin) ||

    //   // Caso 3: día de inicio (y ya pasó hora de inicio)
    //   (soloFechaHoy === soloFechaInicio &&
    //     soloFechaHoy < soloFechaFin &&
    //     minutosAhora >= minutosInicio) ||

    //   // Caso 4: día de fin (y aún no pasa hora de fin)
    //   (soloFechaHoy === soloFechaFin &&
    //     soloFechaHoy > soloFechaInicio &&
    //     minutosAhora <= minutosFin)

    // console.log("✅ ¿Es válida la elección?:", esValida)

    // if (!esValida) {
    //   return response.status(400).json({
    //     message: "La elección no está activa por fechas/horas",
    //     codigo_error: "ELECCION_NO_VALIDA_POR_FECHAS",
    //     detalles: {
    //       fecha_inicio: eleccion.fecha_inicio,
    //       fecha_fin: eleccion.fecha_fin,
    //       hora_inicio: eleccion.hora_inicio,
    //       hora_fin: eleccion.hora_fin,
    //       fecha_actual: hoy.toISODate(),
    //     },
    //   })
    // }



      // 4. Verificar que pertenecen al mismo centro de formación
      if (aprendiz.centro_formacion_idcentro_formacion !== eleccion.idcentro_formacion) {
        return response.status(400).json({
          message: 'El aprendiz y la elección deben pertenecer al mismo centro de formación',
          codigo_error: 'CENTRO_FORMACION_DIFERENTE',
        })
      }

      // 5. Contar candidatos en la elección para información
      const totalCandidatos = await (await import('#models/candidatos')).default
        .query()
        .where('ideleccion', data.elecciones_ideleccion)
        .count('* as total')

      // 6. Verificar que el aprendiz no haya completado ya su voto en esta elección
      const yaVoto = await ValidacionVoto.query()
        .where('aprendiz_idaprendiz', data.aprendiz_idaprendiz)
        .where('elecciones_ideleccion', data.elecciones_ideleccion)
        .where('codigo', 'like', 'VOTED_%') // Solo códigos que indican voto completado
        .first()

      if (yaVoto) {
        return response.status(400).json({
          message: 'Ya has votado en esta elección',
          codigo_error: 'YA_VOTO',
          detalles: {
            fecha_voto: yaVoto.createdAt,
            codigo_validacion: yaVoto.codigo,
          },
        })
      }

      // 6.1. Limpiar OTPs expirados o no utilizados del mismo usuario
      const expirationMinutes = parseInt(process.env.OTP_EXPIRATION_MINUTES || '5')
      const tiempoLimite = DateTime.now().minus({ minutes: expirationMinutes })

      await ValidacionVoto.query()
        .where('aprendiz_idaprendiz', data.aprendiz_idaprendiz)
        .where('elecciones_ideleccion', data.elecciones_ideleccion)
        .where('created_at', '<', tiempoLimite.toSQL())
        .where('codigo', 'not like', 'VOTED_%')
        .where('codigo', 'not like', 'USED_%')
        .delete()

      // 7. Generar código OTP único
      const otpCode = nanoid(6).toUpperCase() // Código de 6 caracteres

      // Crear registro temporal de validación con OTP (SIN candidato_id aún)
      await ValidacionVoto.create({
        codigo: `${otpCode}`,
        aprendiz_idaprendiz: data.aprendiz_idaprendiz,
        elecciones_ideleccion: data.elecciones_ideleccion,
      })

      // 9. Enviar email con OTP
      const emailLimpio = aprendiz.email?.trim()
      const remitente =
        process.env.MAIL_FROM_ADDRESS || process.env.SMTP_FROM_EMAIL || 'noreply@sigeva.com'

      if (!emailLimpio) {
        return response.status(400).json({
          message: 'El aprendiz no tiene un correo registrado. No se puede enviar el código OTP.',
          codigo_error: 'EMAIL_APRENDIZ_VACIO',
        })
      }

      console.log('🔧 Configuración SMTP:', {
        host: process.env.SMTP_HOST,
        port: process.env.SMTP_PORT,
        username: process.env.SMTP_USERNAME,
        from: remitente,
        to: emailLimpio,
      })

      let emailEnviado = false
      try {
        console.log(`📧 Intentando enviar email OTP a: ${emailLimpio}`)

        await mail.send((message) => {
          message
            .to(emailLimpio)
            .from(remitente)
            .subject('Código OTP para Votación - SIGEVA').html(`
              <h2>Código OTP para Votación</h2>
              <p>Hola ${aprendiz.nombres} ${aprendiz.apellidos},</p>
              <p>Tu código OTP es: <strong style="font-size: 24px; color: #007bff;">${otpCode}</strong></p>
              <p>Este código expira en ${expirationMinutes} minutos.</p>
            `)
        })

        emailEnviado = true
        console.log(`✅ Email OTP enviado exitosamente a: ${emailLimpio}`)
      } catch (emailError) {
        console.error('❌ Error completo enviando email OTP:', {
          error: emailError.message,
          code: emailError.code,
          command: emailError.command,
          response: emailError.response,
          responseCode: emailError.responseCode,
        })
      }

      if (!emailEnviado && process.env.NODE_ENV === 'production') {
        return response.status(500).json({
          message:
            'No se pudo enviar el correo con el código. Revisa SMTP en Render (SMTP_HOST, usuario, contraseña y MAIL_FROM_ADDRESS).',
          codigo_error: 'EMAIL_NO_ENVIADO',
        })
      }

      // Respuesta base
      const responseData: any = {
        otp_generado: true,
        email_enviado_a: emailLimpio,
        email_enviado: emailEnviado,
        expira_en_minutos: expirationMinutes,
        eleccion: {
          nombre: eleccion.nombre,
          centro: eleccion.centro?.centro_formacioncol,
          total_candidatos: totalCandidatos[0]?.$extras?.total || 0,
        },
        aprendiz: {
          nombre: `${aprendiz.nombres} ${aprendiz.apellidos}`,
          centro: aprendiz.centro_formacion?.centro_formacioncol,
        },
      }

      // Solo incluir OTP en desarrollo (NODE_ENV !== 'production')
      if (process.env.NODE_ENV !== 'production') {
        responseData.codigo_otp_temporal = otpCode
        responseData._desarrollo_nota =
          'El código OTP se incluye solo en desarrollo. En producción, obtenerlo del email.'
      }

      return response.status(200).json({
        message: 'Código OTP generado exitosamente',
        data: responseData,
      })
    } catch (error) {
      return response.status(500).json({
        message: 'Error al generar OTP',
        error: error.message,
      })
    }
  }

  /**
   * Validar código OTP (NO registra voto)
   */
  async validarOtp({ request, response }: HttpContext) {
    try {
      console.log('📥 Datos recibidos para validación OTP:', request.body())

      const validator = vine.compile(
        vine.object({
          codigo_otp: vine.string().minLength(6).maxLength(6),
        })
      )

      const data = await request.validateUsing(validator)
      console.log('✅ Datos validados:', data)

      // 1. Buscar la validación temporal solo con el código OTP
      const validacionTemporal = await ValidacionVoto.query()
        .where('codigo', data.codigo_otp)
        .first()

      if (!validacionTemporal) {
        return response.status(200).json({
          success: false,
          message: 'Código OTP, aprendiz o elección no coinciden',
        })
      }

      // 2. Verificar que el OTP no haya expirado (usando created_at)
      const tiempoActual = DateTime.now()
      const expirationMinutes = parseInt(process.env.OTP_EXPIRATION_MINUTES || '5')
      const tiempoExpiracion = validacionTemporal.createdAt.plus({ minutes: expirationMinutes })

      if (tiempoActual > tiempoExpiracion) {
        // Eliminar OTP expirado
        await validacionTemporal.delete()

        return response.status(200).json({
          success: false,
          message: 'El código OTP ya expiró. Solicita uno nuevo.',
        })
      }

      // 3. Marcar el OTP como usado (cambiar prefijo)
      await validacionTemporal
        .merge({
          codigo: `USED_${data.codigo_otp}`, // Marcar como usado
        })
        .save()

      return response.status(200).json({
        success: true,
        message: 'Código OTP validado correctamente',
        data: {
          aprendiz_id: validacionTemporal.aprendiz_idaprendiz,
          eleccion_id: validacionTemporal.elecciones_ideleccion,
        },
      })
    } catch (error) {
      console.error('❌ Error en validación OTP:', error)

      // Si es error de validación, devolver detalles específicos
      if (error.messages) {
        return response.status(400).json({
          success: false,
          message: 'Datos de entrada inválidos',
          errors: error.messages,
        })
      }

      return response.status(500).json({
        success: false,
        message: 'Error al validar el código OTP',
        error: error.message,
      })
    }
  }
}
