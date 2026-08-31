import { DateTime } from 'luxon'
import { BaseModel, column } from '@adonisjs/lucid/orm'

export default class RecuperacionPassword extends BaseModel {
  static table = 'recuperacion_password'
  static timestamps = false

  @column({ isPrimary: true })
  declare id: number

  @column()
  declare email: string

  @column()
  declare codigo: string

  @column()
  declare tipo: 'usuario' | 'aprendiz'

  @column({ columnName: 'id_referencia' })
  declare idReferencia: number

  @column.dateTime({ autoCreate: true, columnName: 'created_at' })
  declare createdAt: DateTime

  @column.dateTime({ autoCreate: true, autoUpdate: true, columnName: 'updated_at' })
  declare updatedAt: DateTime
}
