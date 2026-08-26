/** OWNER: PAULA — crear y editar. Body idéntico al Thunder de Alex. Sin jornada. */
import { FormEvent, useState } from 'react'
import { useNavigate, useParams } from 'react-router-dom'
import { actualizarEleccion, crearEleccion } from '@/api/eleccion'
import { getSession } from '@/auth/session'
import type { EleccionBody } from '@/api/types'

function emptyBody(idcentro_formacion: number): EleccionBody {
  return {
    idcentro_formacion,
    nombre: '',
    fecha_inicio: '2026-09-01',
    fecha_fin: '2026-09-05',
    hora_inicio: '2026-09-01T08:00:00.000Z',
    hora_fin: '2026-09-05T16:00:00.000Z',
  }
}

export default function EleccionFormPage() {
  const { id } = useParams()
  const editing = Boolean(id)
  const session = getSession()
  const idcentro = session.rol === 'funcionario' ? session.idcentro_formacion : 1
  const [body, setBody] = useState<EleccionBody>(emptyBody(idcentro))
  const [err, setErr] = useState('')
  const nav = useNavigate()

  async function onSubmit(e: FormEvent) {
    e.preventDefault()
    setErr('')
    try {
      if (editing) {
        await actualizarEleccion(Number(id), body)
      } else {
        await crearEleccion(body)
      }
      nav('/gestion/elecciones')
    } catch (ex) {
      setErr((ex as Error).message)
    }
  }

  return (
    <>
      <p className="owner">OWNER PAULA</p>
      <h2>{editing ? 'Editar elección' : 'Nueva elección del centro'}</h2>
      <p className="lead">
        No hay select de jornada. El centro sale de la sesión, no de un combo de sedes.
      </p>
      <form className="card" onSubmit={onSubmit}>
        <label>Nombre</label>
        <input
          required
          value={body.nombre}
          onChange={(e) => setBody({ ...body, nombre: e.target.value })}
        />
        <div className="row">
          <div>
            <label>fecha_inicio</label>
            <input
              required
              value={body.fecha_inicio}
              onChange={(e) => setBody({ ...body, fecha_inicio: e.target.value })}
            />
          </div>
          <div>
            <label>fecha_fin</label>
            <input
              required
              value={body.fecha_fin}
              onChange={(e) => setBody({ ...body, fecha_fin: e.target.value })}
            />
          </div>
        </div>
        <div className="row">
          <div>
            <label>hora_inicio (ISO)</label>
            <input
              required
              value={body.hora_inicio}
              onChange={(e) => setBody({ ...body, hora_inicio: e.target.value })}
            />
          </div>
          <div>
            <label>hora_fin (ISO)</label>
            <input
              required
              value={body.hora_fin}
              onChange={(e) => setBody({ ...body, hora_fin: e.target.value })}
            />
          </div>
        </div>
        <p className="hint">
          JSON que viaja: idcentro_formacion, nombre, fecha_inicio, fecha_fin, hora_inicio,
          hora_fin. Nunca jornada.
        </p>
        {err ? <p className="err">{err}</p> : null}
        <button type="submit">{editing ? 'Guardar PUT' : 'Crear POST'}</button>
      </form>
    </>
  )
}
