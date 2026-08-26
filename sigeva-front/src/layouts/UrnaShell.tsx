import { NavLink, Outlet } from 'react-router-dom'
import { getSession, setSession } from '@/auth/session'

export default function UrnaShell() {
  const session = getSession()
  const jornada = session.rol === 'aprendiz' ? session.jornada : null
  return (
    <div className="shell">
      <aside className="side">
        <h1>SIGEVA urna</h1>
        <p>
          {session.nombre} · jornada login: {jornada ?? 'null'}
        </p>
        <NavLink to="/urna" className={({ isActive }) => (isActive ? 'active' : '')} end>
          Tarjetón
        </NavLink>
        <p className="tag" style={{ marginTop: 24 }}>
          OWNER Sofia. No armes picker de primer ingreso.
        </p>
        <button
          className="ghost"
          type="button"
          onClick={() =>
            setSession({
              rol: 'funcionario',
              idcentro_formacion: 1,
              nombre: 'Funcionario demo',
            })
          }
        >
          Volver a gestión
        </button>
      </aside>
      <main className="main">
        <Outlet />
      </main>
    </div>
  )
}
