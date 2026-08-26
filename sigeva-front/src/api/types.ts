import type { Jornada } from '@/constants/jornada'

/** Respuesta de POST /api/eleccion/crear y PUT /api/eleccionActualizar/:id */
export type Eleccion = {
  ideleccion: number
  idcentro_formacion: number
  nombre: string
  jornada: string | null
  fecha_inicio: string
  fecha_fin: string
  hora_inicio: string
  hora_fin: string
}

/** Body de crear y de actualizar. NO lleva jornada. */
export type EleccionBody = {
  idcentro_formacion: number
  nombre: string
  fecha_inicio: string
  fecha_fin: string
  hora_inicio: string
  hora_fin: string
}

/** Item de GET /api/eleccionPorCentro/:id — Mebel quita jornada de este objeto. */
export type EleccionCard = {
  ideleccion: number
  titulo: string
  fechaInicio: string
  fechaFin: string
  centro: string
  horaInicio: string
  horaFin: string
}

export type Candidato = {
  idcandidatos: number
  nombres: string
  ideleccion: number
  idaprendiz: number
  propuesta: string
  numero_tarjeton: string
  jornada: Jornada
  foto?: string
}

export type SessionFuncionario = {
  rol: 'funcionario'
  idcentro_formacion: number
  nombre: string
}

export type SessionAprendiz = {
  rol: 'aprendiz'
  nombre: string
  jornada: Jornada | null
}

export type Session = SessionFuncionario | SessionAprendiz
