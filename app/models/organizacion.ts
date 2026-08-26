import { DateTime } from 'luxon'
import { BaseModel, column, hasMany } from '@adonisjs/lucid/orm'
import type { HasMany } from '@adonisjs/lucid/types/relations'
import CentroFormacion from './centro_formacion.js'
import Usuario from './usuario.js'
import Aprendiz from './aprendiz.js'
import Eleccione from './eleccione.js'

export default class Organizacion extends BaseModel {
  public static table = 'organizacion'

  @column({ isPrimary: true })
  declare idorganizacion: number

  @column()
  declare nombre: string

  @column()
  declare slug: string

  @column()
  declare tipo: 'SENA' | 'colegio' | 'universidad' | 'empresa' | 'otro'

  @column()
  declare nit: string | null

  @column()
  declare estado: 'Activo' | 'Suspendido'

  @column.dateTime({ autoCreate: true })
  declare createdAt: DateTime

  @column.dateTime({ autoCreate: true, autoUpdate: true })
  declare updatedAt: DateTime

  @hasMany(() => CentroFormacion, {
    foreignKey: 'idorganizacion',
  })
  declare centros: HasMany<typeof CentroFormacion>

  @hasMany(() => Usuario, {
    foreignKey: 'idorganizacion',
  })
  declare usuarios: HasMany<typeof Usuario>

  @hasMany(() => Aprendiz, {
    foreignKey: 'idorganizacion',
  })
  declare aprendices: HasMany<typeof Aprendiz>

  @hasMany(() => Eleccione, {
    foreignKey: 'idorganizacion',
  })
  declare elecciones: HasMany<typeof Eleccione>
}
