import type { Session } from '@/api/types'

const KEY = 'sigeva.session'

export function getSession(): Session {
  const raw = localStorage.getItem(KEY)
  if (raw) return JSON.parse(raw) as Session
  const funcionario: Session = {
    rol: 'funcionario',
    idcentro_formacion: 1,
    nombre: 'Funcionario demo',
  }
  localStorage.setItem(KEY, JSON.stringify(funcionario))
  return funcionario
}

export function writeSession(session: Session) {
  localStorage.setItem(KEY, JSON.stringify(session))
}

export function setSession(session: Session) {
  writeSession(session)
  window.location.assign(session.rol === 'aprendiz' ? '/urna' : '/gestion/elecciones')
}
