/** OWNER: PAULA — listado. Una card por convocatoria. No pintes jornada. */
import { useEffect, useState } from 'react'
import { Link } from 'react-router-dom'
import { listarTodasPorCentro } from '@/api/eleccion'
import { getSession } from '@/auth/session'
import type { EleccionCard } from '@/api/types'

export default function EleccionesListPage() {
  const session = getSession()
  const idcentro = session.rol === 'funcionario' ? session.idcentro_formacion : 1
  const [rows, setRows] = useState<EleccionCard[]>([])
  const [err, setErr] = useState('')

  useEffect(() => {
    listarTodasPorCentro(idcentro)
      .then((r) => setRows(r.eleccionesActivas ?? []))
      .catch((e: Error) => setErr(e.message))
  }, [idcentro])

  return (
    <>
      <p className="owner">OWNER PAULA</p>
      <h2>Elecciones del centro</h2>
      <p className="lead">
        Una fila por convocatoria. Si el JSON trae jornada, Mebel aún no recortó el GET — no la
        pintes.
      </p>
      <Link to="/gestion/elecciones/nueva">
        <button type="button">Nueva elección</button>
      </Link>
      {err ? <p className="err">{err}</p> : null}
      {rows.map((el) => (
        <article className="card" key={el.ideleccion}>
          <h3>{el.titulo}</h3>
          <p className="tag">
            {el.centro} · {String(el.fechaInicio).slice(0, 10)} → {String(el.fechaFin).slice(0, 10)}
          </p>
          <p className="tag">id {el.ideleccion}</p>
          <Link to={`/gestion/elecciones/${el.ideleccion}/editar`}>Editar</Link>
          {' · '}
          <Link to={`/gestion/elecciones/${el.ideleccion}/candidatos`}>Candidatos (Sofia)</Link>
        </article>
      ))}
    </>
  )
}
