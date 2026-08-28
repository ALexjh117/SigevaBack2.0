import { test } from '@japa/runner'
import {
  esAdminSistema,
  esCentroAjeno,
  esPerfilCanonico,
  esRolDeCentro,
  perfilExigeCentro,
  type ActorSesion,
} from '#services/actor_sesion'

function actorDeCentro(idcentro: number | null): ActorSesion {
  return {
    usuario: {} as ActorSesion['usuario'],
    perfil: 'admin_sistema',
    idcentro,
    esAdminSistema: true,
    esFuncionario: false,
    esAdministrador: false,
    esDeCentro: true,
  }
}

test.group('actor_sesion', () => {
  test('el catálogo cerrado son exactamente 4 perfiles', ({ assert }) => {
    assert.isTrue(esPerfilCanonico('Administrador'))
    assert.isTrue(esPerfilCanonico('Funcionario'))
    assert.isTrue(esPerfilCanonico('Aprendiz'))
    assert.isTrue(esPerfilCanonico('admin_sistema'))
    assert.isFalse(esPerfilCanonico('AdminCentro'))
    assert.isFalse(esPerfilCanonico('admin_sistema_2'))
    assert.isFalse(esPerfilCanonico('Administrador de centro'))
  })

  test('el string del perfil es exacto admin_sistema', ({ assert }) => {
    assert.isTrue(esAdminSistema('admin_sistema'))
    assert.isFalse(esAdminSistema('Administrador'))
    assert.isFalse(esAdminSistema('Admin_Sistema'))
    assert.isTrue(esRolDeCentro('admin_sistema'))
    assert.isTrue(esRolDeCentro('Funcionario'))
    assert.isFalse(esRolDeCentro('Administrador'))
    assert.isTrue(perfilExigeCentro('admin_sistema'))
  })

  test('un admin_sistema no ve el idcentro de otro centro', ({ assert }) => {
    const actor = actorDeCentro(1)
    assert.isTrue(esCentroAjeno(actor, 2))
    assert.isTrue(esCentroAjeno(actor, '2'))
    assert.isFalse(esCentroAjeno(actor, 1))
    assert.isFalse(esCentroAjeno(actor, '1'))
    assert.isFalse(esCentroAjeno(actor, undefined))
    assert.isFalse(esCentroAjeno(actor, null))
    assert.isFalse(esCentroAjeno(null, 2))
  })

  test('sin centro en sesión no se marca ajeno (el 400 lo pone el gate)', ({ assert }) => {
    assert.isFalse(esCentroAjeno(actorDeCentro(null), 2))
  })
})
