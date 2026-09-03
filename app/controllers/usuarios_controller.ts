import { HttpContext } from '@adonisjs/core/http'
import Usuario from '#models/usuario'
import CentroFormacion from '#models/centro_formacion'
import bcrypt from 'bcrypt'
import Perfil from '#models/perfil'
import {
  PERFIL_ADMIN_SISTEMA,
  buscarPerfilCanonico,
  bloquearSiNoEsAdministrador,
  bloquearSiNoPuedeGestionarFuncionarios,
  centroDestinoDeAlta,
  centroYaTieneAdminSistema,
  esAdminSistema,
  esPerfilCanonico,
  perfilExigeCentro,
  resolverActor,
} from '#services/actor_sesion'

export default class UsuariosController {
  async crear({ request, response }: HttpContext) {
    try {
      const actor = await resolverActor(request)
      if (bloquearSiNoEsAdministrador(actor, response)) return

      const { nombres, apellidos, celular, tipo_documento, numero_documento, email, password, estado, idperfil, idcentro_formacion } = request.body()

      const existe = await Usuario.findBy('email', email)
      if (existe) {
        return response.status(400).json({ message: 'El email ya está registrado' })
      }

      const perfilRow = idperfil ? await Perfil.find(idperfil) : null
      if (!perfilRow || !esPerfilCanonico(perfilRow.perfil)) {
        return response.status(400).json({
          message: 'El perfil no es válido. Solo existen Administrador, admin_sistema, Funcionario y Aprendiz',
        })
      }
      if (perfilExigeCentro(perfilRow.perfil) && !idcentro_formacion) {
        return response.status(400).json({
          message: 'El admin_sistema y el funcionario deben tener un centro de formación',
        })
      }
      if (esAdminSistema(perfilRow.perfil) && (await centroYaTieneAdminSistema(Number(idcentro_formacion)))) {
        return response.status(409).json({
          message: 'Este centro de formación ya tiene un admin_sistema',
        })
      }

      const hashpassword = await bcrypt.hash(password, 10)

      const usuario = await Usuario.create({ nombres, apellidos, celular, tipo_documento, numero_documento, email, password: hashpassword, estado, idperfil, idcentro_formacion })

      return response.status(201).json({
        success: true,
        message: 'Usuario registrado exitosamente',
        data: {
          email: usuario.email,
          estado: usuario.estado,
          perfil: perfilRow?.perfil ?? usuario.idperfil,
          centroFormacion: usuario.idcentro_formacion,
        }
      })
    } catch (error) {
      return response.status(500).json({
        success: false,
        message: 'Error interno',
        error: error.message
      })
    }
  }

  async login({ request, response }: HttpContext) {
    try {
      const { email, password } = request.body()

      const usuario = await Usuario.findBy('email', email)
      if (!usuario) {
        return response.status(401).json({ success: false, message: 'Usuario no encontrado' })
      }

      const passwordValido = await bcrypt.compare(password, usuario.password)
      if (!passwordValido) {
        return response.status(200).json({ success: false, message: 'Contraseña incorrecta' })
      }

      if (String(usuario.estado).toLowerCase() !== 'activo') {
        return response.status(401).json({ success: false, message: 'Tu usuario está inactivo' })
      }

      const perfil = await Perfil.findBy('idperfil', usuario.idperfil)
      const nombrePerfil = perfil?.perfil

      if (perfilExigeCentro(nombrePerfil) && !usuario.idcentro_formacion) {
        return response.status(400).json({
          success: false,
          message: 'Tu usuario no tiene centro de formación asignado',
        })
      }

      return response.status(200).json({
        success: true,
        message: 'Login exitoso',
        data: {
          id: usuario.idusuarios,
          email: usuario.email,
          nombres: usuario.nombres,
          apellidos: usuario.apellidos,
          estado: usuario.estado,
          perfil: nombrePerfil,
          centroFormacion: usuario.idcentro_formacion,
        }
      })
    } catch (error) {
      return response.status(500).json({
        success: false,
        message: 'Error interno',
        error: error.message
      })
    }
  }

  async actualizar({ request, response, params }: HttpContext) {
    try {
      const actor = await resolverActor(request)
      if (bloquearSiNoEsAdministrador(actor, response)) return

      const id = params.id
      const usuario = await Usuario.find(id)

      if (!usuario) {
        return response.status(404).json({ success: false, message: 'Usuario no encontrado' })
      }

      const { nombres, apellidos, celular, numero_documento, email, password, estado, idperfil, idcentro_formacion } = request.body()

      // Solo actualiza si se envía un nuevo valor
      if (nombres) usuario.nombres = nombres
      if (apellidos) usuario.apellidos = apellidos
      if (celular) usuario.celular = celular
      if (numero_documento) usuario.numero_documento = numero_documento
      if (email) usuario.email = email
      if (password) usuario.password = await bcrypt.hash(password, 10)
      if (estado !== undefined) usuario.estado = estado
      if (idperfil) usuario.idperfil = idperfil
      if (idcentro_formacion) usuario.idcentro_formacion = idcentro_formacion

      const perfilFinal = await Perfil.find(usuario.idperfil)
      if (!perfilFinal || !esPerfilCanonico(perfilFinal.perfil)) {
        return response.status(400).json({
          success: false,
          message: 'El perfil no es válido. Solo existen Administrador, admin_sistema, Funcionario y Aprendiz',
        })
      }
      if (perfilExigeCentro(perfilFinal.perfil) && !usuario.idcentro_formacion) {
        return response.status(400).json({
          success: false,
          message: 'El admin_sistema y el funcionario deben tener un centro de formación',
        })
      }
      if (
        esAdminSistema(perfilFinal.perfil) &&
        (await centroYaTieneAdminSistema(Number(usuario.idcentro_formacion), usuario.idusuarios))
      ) {
        return response.status(409).json({
          success: false,
          message: 'Este centro de formación ya tiene un admin_sistema',
        })
      }

      await usuario.save()

      return response.status(200).json({
        success: true,
        message: 'Usuario actualizado correctamente',
        data: {
          id: usuario.idusuarios,
          email: usuario.email,
          estado: usuario.estado,
          perfil: perfilFinal?.perfil ?? usuario.idperfil,
          centroFormacion: usuario.idcentro_formacion,
        }
      })
    } catch (error) {
      return response.status(500).json({
        success: false,
        message: 'Error interno al actualizar usuario',
        error: error.message
      })
    }
  }

  async crearFuncionario({ request, response }: HttpContext) {
    try {
      const actor = await resolverActor(request)
      if (bloquearSiNoPuedeGestionarFuncionarios(actor, response) || !actor) return

      const { nombres, apellidos, celular, tipo_documento, numero_documento, email, password, idcentro_formacion } = request.only([
        'nombres',
        'apellidos',
        'celular',
        'tipo_documento',
        'numero_documento',
        'email',
        'password',
        'idcentro_formacion'
      ])

      const required = ['nombres', 'apellidos', 'celular', 'tipo_documento', 'numero_documento', 'email', 'password']
      if (actor.esAdministrador) required.push('idcentro_formacion')

      if (!email || !password || !nombres || !apellidos || !celular || !tipo_documento || !numero_documento) {
        return response.status(400).json({
          error: 'Faltan campos requeridos',
          required,
        })
      }

      const centroId = centroDestinoDeAlta(actor, idcentro_formacion, response)
      if (centroId == null) return

      const centro = await CentroFormacion.find(centroId)
      if (!centro) {
        return response.status(400).json({
          success: false,
          message: 'El centro de formación no existe',
        })
      }

      const perfilFuncionario = await Perfil.findBy('perfil', 'Funcionario')
      if (!perfilFuncionario) {
        return response.status(400).json({
          error: 'Perfil de Funcionario no configurado en el sistema'
        })
      }

      const existe = await Usuario.findBy('email', email)
      if (existe) {
        return response.status(400).json({
          error: 'El correo electrónico ya está registrado'
        })
      }

      const funcionario = await Usuario.create({
        nombres,
        apellidos,
        celular,
        tipo_documento,
        numero_documento,
        email,
        password: await bcrypt.hash(password, 10),
        estado: 'Activo',
        idperfil: perfilFuncionario.idperfil,
        idcentro_formacion: centroId,
      })

      return response.status(201).json({
        success: true,
        message: 'Funcionario creado exitosamente',
        data: {
          id: funcionario.idusuarios,
          nombres: funcionario.nombres,
          apellidos: funcionario.apellidos,
          email: funcionario.email,
          estado: funcionario.estado,
          idcentro_formacion: funcionario.idcentro_formacion,
          centroFormacion: funcionario.idcentro_formacion,
          perfil: 'Funcionario'
        }
      })
    } catch (error) {
      console.error('Error en crearFuncionario:', error)
      return response.status(500).json({
        error: 'Error al crear funcionario',
        details: error.message
      })
    }
  }

  async actualizarFuncionario({ request, response, params }: HttpContext) {
    try {
      const actor = await resolverActor(request)
      if (bloquearSiNoPuedeGestionarFuncionarios(actor, response) || !actor) return

      const funcionario = await Usuario.findOrFail(params.id)
      const perfil = await Perfil.findOrFail(funcionario.idperfil)

      if (perfil.perfil !== 'Funcionario') {
        return response.status(400).json({
          success: false,
          message: 'El usuario no es un funcionario'
        })
      }

      if (actor.esAdminSistema && Number(funcionario.idcentro_formacion) !== actor.idcentro) {
        return response.status(403).json({
          success: false,
          message: 'No puedes consultar ni administrar otro centro de formación',
        })
      }

      const { email, estado, idcentro_formacion } = request.only(['email', 'estado', 'idcentro_formacion'])

      if (email) funcionario.email = email
      if (estado) {
        funcionario.estado = String(estado).toLowerCase().startsWith('inac') ? 'Inactivo' : 'Activo'
      }
      if (idcentro_formacion) {
        if (actor.esAdminSistema && Number(idcentro_formacion) !== actor.idcentro) {
          return response.status(403).json({
            success: false,
            message: 'No puedes reasignar un funcionario a otro centro de formación',
          })
        }
        const centro = await CentroFormacion.find(idcentro_formacion)
        if (!centro) {
          return response.status(400).json({
            success: false,
            message: 'El centro de formación no existe',
          })
        }
        funcionario.idcentro_formacion = idcentro_formacion
      }

      await funcionario.save()

      return response.status(200).json({
        success: true,
        message: 'Funcionario actualizado exitosamente',
        data: {
          id: funcionario.idusuarios,
          email: funcionario.email,
          estado: funcionario.estado,
          idcentro_formacion: funcionario.idcentro_formacion,
          centroFormacion: funcionario.idcentro_formacion,
          perfil: 'Funcionario'
        }
      })
    } catch (error) {
      if (error.code === 'E_ROW_NOT_FOUND') {
        return response.status(404).json({
          success: false,
          message: 'Funcionario no encontrado'
        })
      }
      console.error('Error en actualizarFuncionario:', error)
      return response.status(500).json({
        success: false,
        message: 'Error al actualizar el funcionario',
        error: error.message
      })
    }
  }

  async crearAdminSistema({ request, response }: HttpContext) {
    try {
      const actor = await resolverActor(request)
      if (bloquearSiNoEsAdministrador(actor, response)) return

      const { nombres, apellidos, celular, tipo_documento, numero_documento, email, password, idcentro_formacion } = request.only([
        'nombres',
        'apellidos',
        'celular',
        'tipo_documento',
        'numero_documento',
        'email',
        'password',
        'idcentro_formacion',
      ])

      if (!email || !password || !nombres || !apellidos || !celular || !tipo_documento || !numero_documento) {
        return response.status(400).json({
          error: 'Faltan campos requeridos',
          required: ['nombres', 'apellidos', 'celular', 'tipo_documento', 'numero_documento', 'email', 'password', 'idcentro_formacion'],
        })
      }

      if (!idcentro_formacion) {
        return response.status(400).json({
          message: 'El admin_sistema debe tener un centro de formación',
        })
      }

      const centro = await CentroFormacion.find(idcentro_formacion)
      if (!centro) {
        return response.status(400).json({
          success: false,
          message: 'El centro de formación no existe',
        })
      }

      const perfilAdminSistema = await buscarPerfilCanonico(PERFIL_ADMIN_SISTEMA)
      if (!perfilAdminSistema) {
        return response.status(400).json({
          error: 'Perfil admin_sistema no configurado. Corre database/sql/perfil_admin_sistema.sql',
        })
      }

      if (await centroYaTieneAdminSistema(Number(idcentro_formacion))) {
        return response.status(409).json({
          message: 'Este centro de formación ya tiene un admin_sistema',
        })
      }

      const existe = await Usuario.findBy('email', email)
      if (existe) {
        return response.status(400).json({
          error: 'El correo electrónico ya está registrado',
        })
      }

      const adminCentro = await Usuario.create({
        nombres,
        apellidos,
        celular,
        tipo_documento,
        numero_documento,
        email,
        password: await bcrypt.hash(password, 10),
        estado: 'Activo',
        idperfil: perfilAdminSistema.idperfil,
        idcentro_formacion,
      })

      return response.status(201).json({
        success: true,
        message: 'admin_sistema creado exitosamente',
        data: {
          id: adminCentro.idusuarios,
          nombres: adminCentro.nombres,
          apellidos: adminCentro.apellidos,
          email: adminCentro.email,
          estado: adminCentro.estado,
          idcentro_formacion: adminCentro.idcentro_formacion,
          centroFormacion: adminCentro.idcentro_formacion,
          perfil: PERFIL_ADMIN_SISTEMA,
        },
      })
    } catch (error) {
      if (error.code === '23505') {
        return response.status(409).json({
          message: 'Este centro de formación ya tiene un admin_sistema',
        })
      }
      console.error('Error en crearAdminSistema:', error)
      return response.status(500).json({
        error: 'Error al crear admin_sistema',
        details: error.message,
      })
    }
  }

  async listarFuncionarios({ request, response }: HttpContext) {
    try {
      const actor = await resolverActor(request)
      if (bloquearSiNoPuedeGestionarFuncionarios(actor, response) || !actor) return

      const query = Usuario.query()
        .preload('perfil')
        .whereHas('perfil', (q) => {
          q.where('perfil', 'Funcionario')
        })
        .preload('centro', (c) => {
          c.preload('regional')
        })

      if (actor.esAdminSistema) {
        if (!actor.idcentro) {
          return response.status(400).json({
            success: false,
            message: 'Tu usuario no tiene centro de formación asignado',
          })
        }
        query.where('idcentro_formacion', actor.idcentro)
      }

      const funcionarios = await query

      return response.json(funcionarios.map((f) => ({
        id: f.idusuarios,
        nombres: f.nombres,
        apellidos: f.apellidos,
        celular: f.celular,
        numeroDocumento: f.numero_documento,
        email: f.email,
        estado: f.estado,
        perfil: 'Funcionario',
        idcentro_formacion: f.idcentro_formacion,
        centroFormacion: f.centro,
      })))
    } catch (error) {
      return response.status(500).json({ error: 'Error al listar funcionarios' })
    }
  }

  async listarAdminSistema({ request, response }: HttpContext) {
    try {
      const actor = await resolverActor(request)
      if (bloquearSiNoEsAdministrador(actor, response)) return

      const admins = await Usuario.query()
        .preload('perfil')
        .whereHas('perfil', (q) => {
          q.where('perfil', PERFIL_ADMIN_SISTEMA)
        })
        .preload('centro', (c) => {
          c.preload('regional')
        })

      return response.json(admins.map((u) => ({
        id: u.idusuarios,
        nombres: u.nombres,
        apellidos: u.apellidos,
        celular: u.celular,
        numeroDocumento: u.numero_documento,
        email: u.email,
        estado: u.estado,
        perfil: PERFIL_ADMIN_SISTEMA,
        idcentro_formacion: u.idcentro_formacion,
        centroFormacion: u.centro,
      })))
    } catch (error) {
      return response.status(500).json({ error: 'Error al listar admin_sistema' })
    }
  }
}