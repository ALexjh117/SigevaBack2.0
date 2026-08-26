/**
 * OWNER: SOFIA
 * Candidatos: jornada en el FormData. Urna: ?jornada= en el GET.
 */
import { api } from '@/api/client'
import type { Candidato } from '@/api/types'
import type { Jornada } from '@/constants/jornada'

export async function crearCandidato(form: FormData) {
  return api.postForm('/api/candidatos/crear', form) as Promise<{
    message: string
    data: Candidato
  }>
}

export async function listarCandidatos(ideleccion: number, jornada?: Jornada) {
  const q = jornada ? `?jornada=${encodeURIComponent(jornada)}` : ''
  return api.get(`/api/candidatos/listar/${ideleccion}${q}`) as Promise<{
    message: string
    data: Candidato[]
  }>
}
