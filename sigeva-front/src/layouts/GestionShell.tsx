import { NavLink, Outlet } from 'react-router-dom'
import { getSession, setSession } from '@/auth/session'

export default function GestionShell() {
  const session = getSession()
  return (
    <div className="shell">
      <aside className="side">
        <h1>SIGEVA gestión</h1>
        <p>Funcionario · centro {session.rol === 'funcionario' ? session.idcentro_formacion : '—'}</p>
        <NavLink to="/gestion/elecciones" end className={({ isActive }) => (isActive ? 'active' : '')}>
          Elecciones
        </NavLink>
        <NavLink
          to="/gestion/elecciones/nueva"
          className={({ isActive }) => (isActive ? 'active' : '')}
        >
          Nueva elección
        </NavLink>
        <p className="tag" style={{ marginTop: 24 }}>
          Paula: elecciones. Sofia: candidatos (entra desde una card).
        </p>
        <button
          className="ghost"
          type="button"
          onClick={() =>
            setSession({ rol: 'aprendiz', nombre: 'Aprendiz Tarde', jornada: 'Tarde' })
          }
        >
          Cambiar a urna (Tarde)
        </button>
      </aside>
      <main className="main">
        <Outlet />
      </main>
    </div>
  )
}
