import AuthController from '#controllers/auth_controller'
import UsuariosController from '#controllers/usuarios_controller'
import router from '@adonisjs/core/services/router'

const user = new UsuariosController()
const auth = new AuthController()

// Rutas para Funcionarios
router.post('/api/usuarios/funcionarios', user.crearFuncionario)
router.put('/api/usuarios/funcionarios/:id', user.actualizarFuncionario)
router.get('/api/usuarios/funcionarios', user.listarFuncionarios)

router.post('/api/usuarios/admin-sistema', user.crearAdminSistema)
router.get('/api/usuarios/admin-sistema', user.listarAdminSistema)

// Rutas generales de usuarios (manteniendo las existentes)
router.post('/api/usuarios/crear', user.crear)
router.post('/api/usuarios/login', user.login)
router.put('/api/usuarios/:id', user.actualizar)

router.get('/api/auth/me', auth.me)
router.post('/api/auth/logout', auth.logout)