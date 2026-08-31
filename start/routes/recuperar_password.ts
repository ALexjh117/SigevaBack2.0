import router from '@adonisjs/core/services/router'
import RecuperacionPasswordController from '#controllers/recuperacion_password_controller'

const recuperacionPassword = new RecuperacionPasswordController()

router
  .group(() => {
    router.post('/solicitar', recuperacionPassword.solicitar)
    router.post('/confirmar', recuperacionPassword.confirmar)
  })
  .prefix('/api/recuperar-password')
