import { test } from '@japa/runner'
import { esRutaPublica, firmarJwt, verificarJwt } from '#services/auth_jwt'

test.group('auth_jwt', () => {
  test('firma y verifica un JWT de usuario', ({ assert }) => {
    const token = firmarJwt({ sub: 12, typ: 'usuario', perfil: 'Administrador' })
    const payload = verificarJwt(token)
    assert.isNotNull(payload)
    assert.equal(payload?.sub, 12)
    assert.equal(payload?.typ, 'usuario')
    assert.equal(payload?.perfil, 'Administrador')
  })

  test('rechaza un JWT manipulado', ({ assert }) => {
    const token = firmarJwt({ sub: 1, typ: 'aprendiz', perfil: 'Aprendiz' })
    const roto = `${token.slice(0, -2)}aa`
    assert.isNull(verificarJwt(roto))
  })

  test('login, recuperar password, logout y docs son públicos', ({ assert }) => {
    assert.isTrue(esRutaPublica('POST', '/api/usuarios/login'))
    assert.isTrue(esRutaPublica('POST', '/api/aprendiz/login/'))
    assert.isTrue(esRutaPublica('POST', '/api/recuperar-password/solicitar'))
    assert.isTrue(esRutaPublica('POST', '/api/auth/logout'))
    assert.isTrue(esRutaPublica('GET', '/docs'))
    assert.isTrue(esRutaPublica('GET', '/docs-json'))
    assert.isFalse(esRutaPublica('GET', '/api/usuarios/funcionarios'))
    assert.isFalse(esRutaPublica('POST', '/api/eleccion/crear'))
  })
})
