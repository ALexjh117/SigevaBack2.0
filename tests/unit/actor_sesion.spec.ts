import { test } from '@japa/runner'
import {
  bloquearRedFuncionarios,
  bloquearSiNoEsAdministrador,
  bloquearSiNoPuedeGestionarFuncionarios,
  centroDestinoDeAlta,
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

function actorAdministrador(): ActorSesion {
  return {
    usuario: {} as ActorSesion['usuario'],
    perfil: 'Administrador',
    idcentro: null,
    esAdminSistema: false,
    esFuncionario: false,
    esAdministrador: true,
    esDeCentro: false,
  }
}

function actorFuncionario(idcentro: number): ActorSesion {
  return {
    usuario: {} as ActorSesion['usuario'],
    perfil: 'Funcionario',
    idcentro,
    esAdminSistema: false,
    esFuncionario: true,
    esAdministrador: false,
    esDeCentro: true,
  }
}

function mockResponse() {
  const res: {
    statusCode: number
    payload: unknown
    status: (code: number) => typeof res
    json: (body: unknown) => typeof res
  } = {
    statusCode: 200,
    payload: null,
    status(code: number) {
      this.statusCode = code
      return this
    },
    json(body: unknown) {
      this.payload = body
      return this
    },
  }
  return res
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

  test('solo el Administrador de red crea admin_sistema', ({ assert }) => {
    const ok = mockResponse()
    assert.isFalse(bloquearSiNoEsAdministrador(actorAdministrador(), ok as any))
    assert.equal(ok.statusCode, 200)

    const noActor = mockResponse()
    assert.isTrue(bloquearSiNoEsAdministrador(null, noActor as any))
    assert.equal(noActor.statusCode, 401)

    const centro = mockResponse()
    assert.isTrue(bloquearSiNoEsAdministrador(actorDeCentro(1), centro as any))
    assert.equal(centro.statusCode, 403)

    const mesa = mockResponse()
    assert.isTrue(bloquearSiNoEsAdministrador(actorFuncionario(1), mesa as any))
    assert.equal(mesa.statusCode, 403)
  })

  test('Administrador y admin_sistema gestionan funcionarios; el de mesa no', ({ assert }) => {
    const admin = mockResponse()
    assert.isFalse(bloquearSiNoPuedeGestionarFuncionarios(actorAdministrador(), admin as any))

    const sede = mockResponse()
    assert.isFalse(bloquearSiNoPuedeGestionarFuncionarios(actorDeCentro(1), sede as any))

    const sinCentro = mockResponse()
    assert.isTrue(bloquearSiNoPuedeGestionarFuncionarios(actorDeCentro(null), sinCentro as any))
    assert.equal(sinCentro.statusCode, 400)

    const mesa = mockResponse()
    assert.isTrue(bloquearSiNoPuedeGestionarFuncionarios(actorFuncionario(1), mesa as any))
    assert.equal(mesa.statusCode, 403)
  })

  test('el funcionario de mesa no lista la red de jurados; admin_sistema sí lista los de su sede', ({ assert }) => {
    const mesa = mockResponse()
    assert.isTrue(bloquearRedFuncionarios(actorFuncionario(1), mesa as any))
    assert.equal(mesa.statusCode, 403)

    const sede = mockResponse()
    assert.isFalse(bloquearRedFuncionarios(actorDeCentro(1), sede as any))

    const red = mockResponse()
    assert.isFalse(bloquearRedFuncionarios(actorAdministrador(), red as any))
  })

  test('centro destino: admin_sistema usa el de sesión; Administrador debe enviarlo', ({ assert }) => {
    const sedeOk = mockResponse()
    assert.equal(centroDestinoDeAlta(actorDeCentro(7), undefined, sedeOk as any), 7)

    const sedeAjeno = mockResponse()
    assert.isNull(centroDestinoDeAlta(actorDeCentro(7), 99, sedeAjeno as any))
    assert.equal(sedeAjeno.statusCode, 403)

    const redOk = mockResponse()
    assert.equal(centroDestinoDeAlta(actorAdministrador(), 3, redOk as any), 3)

    const redSinCentro = mockResponse()
    assert.isNull(centroDestinoDeAlta(actorAdministrador(), undefined, redSinCentro as any))
    assert.equal(redSinCentro.statusCode, 400)
  })
})
