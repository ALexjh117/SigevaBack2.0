import { test } from '@japa/runner'
import { DateTime } from 'luxon'
import {
  minutosExpiracionOtp,
  normalizarEmail,
  otpExpirado,
} from '#services/recuperacion_password'

test.group('recuperacion_password', () => {
  test('normaliza el correo recortando espacios y bajando mayúsculas', ({ assert }) => {
    assert.equal(normalizarEmail('  Ana.Perez@SENA.edu.co  '), 'ana.perez@sena.edu.co')
  })

  test('la caducidad por defecto son 5 minutos', ({ assert }) => {
    assert.equal(minutosExpiracionOtp(), 5)
  })

  test('un código de hace 6 minutos ya expiró', ({ assert }) => {
    const creado = DateTime.now().minus({ minutes: 6 })
    assert.isTrue(otpExpirado(creado))
  })

  test('un código de hace 1 minuto sigue vigente', ({ assert }) => {
    const creado = DateTime.now().minus({ minutes: 1 })
    assert.isFalse(otpExpirado(creado))
  })
})
