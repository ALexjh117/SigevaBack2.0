// app/Middleware/ValidarVotoUnico.ts
import { HttpContext } from '@adonisjs/core/http'
import Votoxcandidato from '#models/votoxcandidato'
import { idAprendizDeLaPeticion } from '#services/auth_jwt'

export default class ValidarVotoUnico {
  public async handle({ request, response }: HttpContext, next: () => Promise<void>) {
    const idAprendiz = idAprendizDeLaPeticion(request)
    const idEleccion = request.input('ideleccion')

    if (!idAprendiz) {
      return response.status(403).json({
        success: false,
        message: 'Inicia sesión como aprendiz para votar',
      })
    }

    if (!idEleccion) {
      return response.status(200).json({
        message: 'Debes enviar ideleccion en la petición',
      })
    }

    // 2. Buscar si ya existe un voto de ese aprendiz en esa elección
    const votoExistente = await Votoxcandidato
      .query()
      .where('idaprendiz', idAprendiz)
      .preload('candidato', (candidatoQuery) => {
        candidatoQuery.where('ideleccion', idEleccion) 
      })
    // 3. Verificar si efectivamente tiene algún voto en esa elección
    const yaVoto = votoExistente.some((v) => v.candidato?.ideleccion === idEleccion)

    if (yaVoto) {
      return response.status(200).json({succes:false,
        message: `Ya realizaste un voto en esta elección.`,
      })
    }

    // 4. Continuar si no existe voto previo
    await next()
  }
}
