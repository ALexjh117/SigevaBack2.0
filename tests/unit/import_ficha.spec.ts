import { test } from '@japa/runner'
import {
  normalizarDocumento,
  normalizarEmail,
  normalizarJornada,
  normalizarNombrePrograma,
  parseFichaCaracterizacion,
} from '#services/import_ficha'

test.group('import_ficha Sofia Plus', () => {
  test('C2 de la ficha 2992857 separa grupo y programa', ({ assert }) => {
    const parsed = parseFichaCaracterizacion('2992857 - AUTOMATIZACION DE SISTEMAS MECATRONICOS')
    assert.equal(parsed.numeroGrupo, '2992857')
    assert.equal(parsed.nombrePrograma, 'AUTOMATIZACION DE SISTEMAS MECATRONICOS')
  })

  test('C2 con punto final no duplica el programa', ({ assert }) => {
    const parsed = parseFichaCaracterizacion('2923604 - ANALISIS Y DESARROLLO DE SOFTWARE.')
    assert.equal(parsed.numeroGrupo, '2923604')
    assert.equal(parsed.nombrePrograma, 'ANALISIS Y DESARROLLO DE SOFTWARE')
    assert.equal(normalizarNombrePrograma('ANALISIS Y DESARROLLO DE SOFTWARE.'), 'ANALISIS Y DESARROLLO DE SOFTWARE')
  })

  test('guion largo de Excel también sirve', ({ assert }) => {
    const parsed = parseFichaCaracterizacion('2469519 – CATASTRO')
    assert.equal(parsed.numeroGrupo, '2469519')
    assert.equal(parsed.nombrePrograma, 'CATASTRO')
  })

  test('C2 vacío o ilegible no inventa ficha', ({ assert }) => {
    assert.equal(parseFichaCaracterizacion('').numeroGrupo, '')
    assert.equal(parseFichaCaracterizacion('Ficha de Caracterización:').numeroGrupo, '')
  })

  test('jornada canónica con ñ y Nocturna = Noche', ({ assert }) => {
    assert.equal(normalizarJornada('Mañana'), 'Mañana')
    assert.equal(normalizarJornada('tarde'), 'Tarde')
    assert.equal(normalizarJornada('Noche'), 'Noche')
    assert.equal(normalizarJornada('Nocturna'), 'Noche')
    assert.isNull(normalizarJornada('vespertina'))
  })

  test('el documento numérico del Excel queda como texto para la clave', ({ assert }) => {
    assert.equal(normalizarDocumento(1004573481), '1004573481')
    assert.equal(normalizarDocumento(' 1004573481 '), '1004573481')
    assert.equal(normalizarEmail('  DanielZ@Gmail.com '), 'danielz@gmail.com')
  })
})
