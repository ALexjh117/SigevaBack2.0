/* eslint-disable @unicorn/filename-case */
/* eslint-disable prettier/prettier */
import Eleccione from "#models/eleccione";

export default class FiltrarService {
    [x: string]: any;
    async filtroElecciones( idCentro_formacion: number, jornada: string ){
        const filterToday = new Date()

        const elecciones = await Eleccione.query()
        .if(idCentro_formacion, (consultar)=> {
            consultar.where('idCentro_formacion', idCentro_formacion)
        })

        .where('fecha_inicio', '<=', filterToday)
        .where('fecha_fin', '>=', filterToday)
        .preload('candidato',  (consultarCandidatos) => {
            if (jornada) {
                consultarCandidatos.where('jornada', jornada)
            }
            consultarCandidatos.preload('aprendiz')
        })

        return elecciones
    }
}
