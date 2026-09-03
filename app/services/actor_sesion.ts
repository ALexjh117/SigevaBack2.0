/**
 * HU-S2-030 — aislamiento por centro de formación.
 *
 * Roles:
 * - Aprendiz: urna de su centro. No administra.
 * - Funcionario: opera la mesa de UN centro. No crea pares ni admin_sistema.
 * - admin_sistema: administra UN centro (elecciones, padrón, import de su sede,
 *   alta de funcionarios de SU sede). Centro obligatorio. No ve tablero de red,
 *   no lista funcionarios de toda la red, no importa eligiendo otra sede, no vota.
 * - Administrador: gobierno de la red. Crea admin_sistema y funcionarios
 *   eligiendo el centro. Importa aprendices eligiendo el centro. Ve todo.
 *
 * Fuente del centro: usuarios.idcentro_formacion (sesión).
 * El cliente manda x-user-id o userId (mismo patrón que el import Excel).
 * Sin JWT. Si el cliente manda otro idcentro, se ignora o 403. Nunca filas ajenas.
 */
import Usuario from '#models/usuario'
import Perfil from '#models/perfil'
import type { HttpContext } from '@adonisjs/core/http'

export const PERFIL_ADMIN_SISTEMA = 'admin_sistema'

/** Catálogo cerrado. No se crea un quinto rol ni se duplica admin_sistema. */
export const PERFILES_CANONICOS = [
  'Administrador',
  'Funcionario',
  'Aprendiz',
  PERFIL_ADMIN_SISTEMA,
] as const

export type PerfilCanonico = (typeof PERFILES_CANONICOS)[number]

export type ActorSesion = {
  usuario: Usuario
  perfil: string
  idcentro: number | null
  esAdminSistema: boolean
  esFuncionario: boolean
  esAdministrador: boolean
  esDeCentro: boolean
}

export function esAdminSistema(perfil?: string | null) {
  return perfil === PERFIL_ADMIN_SISTEMA
}

export function esFuncionario(perfil?: string | null) {
  return perfil?.toLowerCase() === 'funcionario'
}

export function esAdministrador(perfil?: string | null) {
  return perfil?.toLowerCase() === 'administrador'
}

export function esRolDeCentro(perfil?: string | null) {
  return esAdminSistema(perfil) || esFuncionario(perfil)
}

export function perfilExigeCentro(perfil?: string | null) {
  return esRolDeCentro(perfil)
}

export function esPerfilCanonico(perfil?: string | null): perfil is PerfilCanonico {
  return (PERFILES_CANONICOS as readonly string[]).includes(perfil ?? '')
}

export async function buscarPerfilCanonico(nombre: string) {
  const row = await Perfil.findBy('perfil', nombre)
  if (!row || !esPerfilCanonico(row.perfil)) return null
  return row
}

export async function centroYaTieneAdminSistema(idcentro: number, exceptUserId?: number) {
  const perfil = await buscarPerfilCanonico(PERFIL_ADMIN_SISTEMA)
  if (!perfil) return false
  const query = Usuario.query()
    .where('idperfil', perfil.idperfil)
    .where('idcentro_formacion', idcentro)
  if (exceptUserId) {
    query.whereNot('idusuarios', exceptUserId)
  }
  return Boolean(await query.first())
}

function leerUserId(request: HttpContext['request']): number | null {
  const raw = request.header('x-user-id') ?? request.input('userId') ?? request.qs().userId
  if (raw === undefined || raw === null || raw === '') return null
  const id = Number(raw)
  return Number.isInteger(id) && id > 0 ? id : null
}

function centroDeUsuario(usuario: Usuario): number | null {
  const n = Number(usuario.idcentro_formacion)
  return Number.isInteger(n) && n > 0 ? n : null
}

export async function resolverActor(request: HttpContext['request']): Promise<ActorSesion | null> {
  const id = leerUserId(request)
  if (!id) return null

  const usuario = await Usuario.query().where('idusuarios', id).preload('perfil').first()
  if (!usuario) return null

  const perfil = usuario.perfil?.perfil ?? ''
  return {
    usuario,
    perfil,
    idcentro: centroDeUsuario(usuario),
    esAdminSistema: esAdminSistema(perfil),
    esFuncionario: esFuncionario(perfil),
    esAdministrador: esAdministrador(perfil),
    esDeCentro: esRolDeCentro(perfil),
  }
}

export function esCentroAjeno(actor: ActorSesion | null, idPedido: unknown): boolean {
  if (!actor?.esDeCentro || actor.idcentro == null) return false
  if (idPedido === undefined || idPedido === null || idPedido === '') return false
  const n = Number(idPedido)
  if (!Number.isInteger(n) || n <= 0) return false
  return n !== actor.idcentro
}

export function bloquearSiCentroAjeno(
  actor: ActorSesion | null,
  idPedido: unknown,
  response: HttpContext['response']
): boolean {
  if (actor?.esDeCentro && !actor.idcentro) {
    response.status(400).json({
      message: 'Tu usuario no tiene centro de formación asignado',
    })
    return true
  }
  if (esCentroAjeno(actor, idPedido)) {
    response.status(403).json({
      message: 'No puedes consultar ni administrar otro centro de formación',
    })
    return true
  }
  return false
}

export function bloquearTableroRed(
  actor: ActorSesion | null,
  response: HttpContext['response']
): boolean {
  if (actor?.esDeCentro) {
    response.status(403).json({
      message: 'No tienes permiso para el tablero de red',
    })
    return true
  }
  return false
}

export function bloquearSiFaltaActor(
  actor: ActorSesion | null,
  response: HttpContext['response']
): actor is null {
  if (!actor) {
    response.status(400).json({
      success: false,
      message: 'Falta userId en el body o x-user-id',
    })
    return true
  }
  return false
}

export function bloquearSiNoEsAdministrador(
  actor: ActorSesion | null,
  response: HttpContext['response']
): boolean {
  if (bloquearSiFaltaActor(actor, response)) return true
  if (!actor.esAdministrador) {
    response.status(403).json({
      success: false,
      message: 'Solo el Administrador de red puede hacer esta operación',
    })
    return true
  }
  return false
}

/** Administrador de red o admin_sistema de un centro. El funcionario de mesa no. */
export function bloquearSiNoPuedeGestionarFuncionarios(
  actor: ActorSesion | null,
  response: HttpContext['response']
): boolean {
  if (bloquearSiFaltaActor(actor, response)) return true
  if (actor.esAdministrador) return false
  if (actor.esAdminSistema) {
    if (!actor.idcentro) {
      response.status(400).json({
        success: false,
        message: 'Tu usuario no tiene centro de formación asignado',
      })
      return true
    }
    return false
  }
  response.status(403).json({
    success: false,
    message: 'No tienes permiso para gestionar funcionarios',
  })
  return true
}

/**
 * Centro destino al crear funcionario o al importar.
 * admin_sistema / funcionario: el de la sesión (otro id = 403).
 * Administrador: debe enviar el id (si no = 400).
 */
export function centroDestinoDeAlta(
  actor: ActorSesion,
  idPedido: unknown,
  response: HttpContext['response']
): number | null {
  if (actor.esDeCentro) {
    if (!actor.idcentro) {
      response.status(400).json({
        success: false,
        message: 'Tu usuario no tiene centro de formación asignado',
      })
      return null
    }
    if (esCentroAjeno(actor, idPedido)) {
      response.status(403).json({
        success: false,
        message: 'No puedes consultar ni administrar otro centro de formación',
      })
      return null
    }
    return actor.idcentro
  }

  const n = Number(idPedido)
  if (!Number.isInteger(n) || n <= 0) {
    response.status(400).json({
      success: false,
      message: 'Debes enviar idcentro_formacion (administrador de red)',
    })
    return null
  }
  return n
}

/** El funcionario de mesa no lista jurados. admin_sistema lista SOLO los de su sede. */
export function bloquearRedFuncionarios(
  actor: ActorSesion | null,
  response: HttpContext['response']
): boolean {
  if (actor?.esFuncionario) {
    response.status(403).json({
      success: false,
      message: 'No tienes permiso para listar funcionarios de toda la red',
    })
    return true
  }
  return false
}

export function centroDeLaSesion(actor: ActorSesion | null): number | null {
  if (actor?.esDeCentro) return actor.idcentro
  return null
}
