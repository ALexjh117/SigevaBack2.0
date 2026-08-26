/** OWNER: SOFIA — form candidato + tres bloques. Paula no entra aquí. */
import { FormEvent, useEffect, useState } from 'react'
import { useParams } from 'react-router-dom'
import { crearCandidato, listarCandidatos } from '@/api/candidatos'
import type { Candidato } from '@/api/types'
import { JORNADAS, type Jornada } from '@/constants/jornada'

export default function CandidatosGestionPage() {
  const { id } = useParams()
  const ideleccion = Number(id)
  const [list, setList] = useState<Candidato[]>([])
  const [err, setErr] = useState('')
  const [jornada, setJornada] = useState<Jornada>('Tarde')

  async function reload() {
    const r = await listarCandidatos(ideleccion)
    setList(r.data ?? [])
  }

  useEffect(() => {
    reload().catch((e: Error) => setErr(e.message))
  }, [ideleccion])

  async function onSubmit(e: FormEvent<HTMLFormElement>) {
    e.preventDefault()
    setErr('')
    const f = e.currentTarget
    const fd = new FormData()
    fd.append('ideleccion', String(ideleccion))
    fd.append('idaprendiz', (f.elements.namedItem('idaprendiz') as HTMLInputElement).value)
    fd.append('nombres', (f.elements.namedItem('nombres') as HTMLInputElement).value)
    fd.append('propuesta', (f.elements.namedItem('propuesta') as HTMLInputElement).value)
    fd.append('numero_tarjeton', (f.elements.namedItem('numero_tarjeton') as HTMLInputElement).value)
    fd.append('jornada', jornada)
    const foto = (f.elements.namedItem('foto') as HTMLInputElement).files?.[0]
    if (foto) fd.append('foto', foto)
    try {
      await crearCandidato(fd)
      f.reset()
      await reload()
    } catch (ex) {
      setErr((ex as Error).message)
    }
  }

  return (
    <>
      <p className="owner sofia">OWNER SOFIA</p>
      <h2>Candidatos de la elección {ideleccion}</h2>
      <p className="lead">
        GET sin query = los tres bloques. El select jornada es NUEVO. Grafía exacta del enum.
      </p>
      <form className="card" onSubmit={onSubmit}>
        <div className="row">
          <div>
            <label>idaprendiz</label>
            <input name="idaprendiz" required defaultValue="401" />
          </div>
          <div>
            <label>nombres</label>
            <input name="nombres" required defaultValue="Ana Pérez" />
          </div>
        </div>
        <label>propuesta</label>
        <input name="propuesta" required defaultValue="Más bienestar en talleres" />
        <div className="row">
          <div>
            <label>numero_tarjeton</label>
            <input name="numero_tarjeton" required defaultValue="01" />
          </div>
          <div>
            <label>jornada</label>
            <select value={jornada} onChange={(e) => setJornada(e.target.value as Jornada)} required>
              {JORNADAS.map((j) => (
                <option key={j} value={j}>
                  {j}
                </option>
              ))}
            </select>
          </div>
        </div>
        <label>foto (opcional)</label>
        <input name="foto" type="file" accept="image/*" />
        {err ? <p className="err">{err}</p> : null}
        <button type="submit">POST /api/candidatos/crear</button>
      </form>
      <div className="blocks">
        {JORNADAS.map((j) => (
          <section className="card" key={j}>
            <h3>{j}</h3>
            {list
              .filter((c) => c.jornada === j)
              .map((c) => (
                <p key={c.idcandidatos}>
                  #{c.numero_tarjeton} {c.nombres}
                </p>
              ))}
          </section>
        ))}
      </div>
    </>
  )
}
