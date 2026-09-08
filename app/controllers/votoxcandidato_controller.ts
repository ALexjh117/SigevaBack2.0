import { HttpContext } from '@adonisjs/core/http'
import Votoxcandidato from '#models/votoxcandidato'
import { idAprendizDeLaPeticion } from '#services/auth_jwt'



export default class    VotoxcandidatoController {

    async crear({ request, response }: HttpContext) {
        try {
            const idaprendiz = idAprendizDeLaPeticion(request)
            if (!idaprendiz) {
                return response.status(403).json({
                    success: false,
                    mensaje: 'Inicia sesión como aprendiz para votar',
                })
            }
            const data = request.only(['idcandidatos', 'contador'])
            await Votoxcandidato.create({
                idcandidatos: data.idcandidatos,
                contador: data.contador,
                idaprendiz,
            })
            return response.status(201).json({ mensaje: "Éxito" })
        } catch (error) {
            return response.status(500).json({ mensaje: "Error", error: error.message })
        }
    }

    async getAll({ response }: HttpContext) {
        try {
            const voticos = await Votoxcandidato.all()
            return response.status(200).json({ mensaje: "Éxito", data: voticos })
        } catch (error) {
            return response.status(500).json({ mensaje: "Error", error: error.message })
        }
    }

    async quantityVotes({ response, params }: HttpContext) {
        const {id} =params
        try{
            const totalVotos = await Votoxcandidato.query().where('idcandidatos', id).count('* as total')
            response.status(200).json({mensaje: "Éxito", votos: totalVotos[0].$extras.total})
        }catch (error) {
            return response.status(500).json({ mensaje: "Error", error: error.message })
        }
    }

}