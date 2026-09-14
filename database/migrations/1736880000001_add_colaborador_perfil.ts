import { BaseSchema } from '@adonisjs/lucid/schema'

export default class extends BaseSchema {
  protected tableName = 'perfil'

  public async up () {
    this.defer(async (knex) => {
      await knex.raw(`
        INSERT INTO perfil (idperfil, perfil)
        SELECT COALESCE((SELECT MAX(idperfil) FROM perfil), 0) + 1, 'colaborador'
        WHERE NOT EXISTS (SELECT 1 FROM perfil WHERE perfil = 'colaborador')
      `)
    })
  }

  public async down () {
    this.defer(async () => {
      await this.db.from('perfil').where('perfil', 'colaborador').delete()
    })
  }
}