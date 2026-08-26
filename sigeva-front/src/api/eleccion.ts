/**
 * OWNER: PAULA
 * Crear / editar / listar elección. Nunca mandes jornada.
 */
import { api } from '@/api/client'
import type { Eleccion, EleccionBody, EleccionCard } from '@/api/types'

export async function crearEleccion(body: EleccionBody) {
  return api.postJson('/api/eleccion/crear', body) as Promise<{
    message: string
    eleccion: Eleccion
  }>
}

export async function actualizarEleccion(idEleccion: number, body: EleccionBody) {
  return api.putJson(`/api/eleccionActualizar/${idEleccion}`, body) as Promise<{
    message: string
    eleccion: Eleccion
  }>
}

export async function listarPorCentro(idcentro: number) {
  return api.get(`/api/eleccionPorCentro/${idcentro}`) as Promise<{
    message: string
    eleccionesActivas: EleccionCard[]
  }>
}

export async function listarTodasPorCentro(idcentro: number) {
  return api.get(`/api/eleccion/traerTodas/${idcentro}`) as Promise<{
    message: string
    eleccionesActivas: EleccionCard[]
  }>
}
