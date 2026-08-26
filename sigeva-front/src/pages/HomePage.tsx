import { Link } from 'react-router-dom'
import { writeSession } from '@/auth/session'

export default function HomePage() {
  return (
    <div className="main" style={{ maxWidth: 880, margin: '0 auto' }}>
      <p className="owner">CONTRATO PARA EL AGENTE DE FRONTEND</p>
      <h2>SIGEVA — elección global</h2>
      <p className="lead">
        Este React no es el repo de producción. Es la estructura y el contrato HTTP para que
        asignes a Paula (elección) y a Sofia (candidato + urna). Lee AGENTS.md antes de codear.
      </p>
      <div className="home-grid">
        <Link
          className="card"
          to="/gestion/elecciones"
          onClick={() =>
            writeSession({
              rol: 'funcionario',
              idcentro_formacion: 1,
              nombre: 'Funcionario demo',
            })
          }
        >
          <p className="owner">PAULA</p>
          <h3>Gestión · elecciones</h3>
          <p className="tag">Form sin jornada. Una card por convocatoria. POST/PUT de Alex.</p>
        </Link>
        <Link
          className="card"
          to="/urna"
          onClick={() =>
            writeSession({ rol: 'aprendiz', nombre: 'Aprendiz Tarde', jornada: 'Tarde' })
          }
        >
          <p className="owner sofia">SOFIA</p>
          <h3>Urna · tarjetón</h3>
          <p className="tag">GET candidatos?jornada=Tarde. Sin modal de elegir jornada.</p>
        </Link>
      </div>
    </div>
  )
}
