/** Cadenas EXACTAS del back (Vine + PostgreSQL). Con eñe. No uses "manana". */
export const JORNADAS = ['Mañana', 'Tarde', 'Noche'] as const
export type Jornada = (typeof JORNADAS)[number]
