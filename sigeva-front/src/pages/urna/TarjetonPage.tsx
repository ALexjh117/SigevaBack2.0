/** OWNER: SOFIA — urna. GET con ?jornada= del login. Sin picker de primer ingreso. */
import { useEffect, useState } from 'react'
import { listarCandidatos } from '@/api/candidatos'
import { getSession } from '@/auth/session'
import type { Candidato } from '@/api/types'

const IDELECCION_DEMO = 12

export default function TarjetonPage() {
  const session = getSession()
  const jornada = session.rol === 'aprendiz' ? session.jornada : null
  const [list, setList] = useState<Candidato[]>([])
  const [err, setErr] = useState('')
  const [id, setId] = useState(IDELECCION_DEMO)

  useEffect(() => {
    if (!jornada) {
      setErr('Login sin jornada. No armes modal: eso es el último paquete.')
      return
    }
    listarCandidatos(id, jornada)
      .then((r) => setList(r.data ?? []))
      .catch((e: Error) => setErr(e.message))
  }, [id, jornada])

  return (
    <>
      <p className="owner sofia">OWNER SOFIA · URNA</p>
      <h2>Tarjetón</h2>
      <p className="lead">
        Una elección del centro. El recorte lo hace ?jornada={jornada ?? '—'}. No listes tres
        elecciones.
      </p>
      <label>ideleccion</label>
      <input type="number" value={id} onChange={(e) => setId(Number(e.target.value))} />
      {err ? <p className="err">{err}</p> : null}
      <div className="tarjeton">
        {list.map((c) => (
          <article className="card" key={c.idcandidatos}>
            <p className="tag">#{c.numero_tarjeton} · {c.jornada}</p>
            <h3>{c.nombres}</h3>
            <p>{c.propuesta}</p>
          </article>
        ))}
      </div>
    </>
  )
}
