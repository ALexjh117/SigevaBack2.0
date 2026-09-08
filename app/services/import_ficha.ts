export const JORNADAS_CANONICAS = ['Mañana', 'Tarde', 'Noche'] as const
export type JornadaCanon = (typeof JORNADAS_CANONICAS)[number]

/** C2 de Sofia Plus: "2992857 - AUTOMATIZACION DE SISTEMAS MECATRONICOS" */
export function parseFichaCaracterizacion(c2: unknown) {
  const limpia = String(c2 ?? '')
    .replace(/[–—]/g, '-')
    .trim()
  const match = limpia.match(/^(\d+)\s*-\s*(.+)$/)
  if (!match) {
    return { numeroGrupo: '', nombrePrograma: '' }
  }
  return {
    numeroGrupo: match[1],
    nombrePrograma: normalizarNombrePrograma(match[2]),
  }
}

export function normalizarNombrePrograma(nombre: string) {
  return nombre.replace(/\.+$/, '').trim()
}

export function normalizarJornada(raw?: string | null): JornadaCanon | null {
  const n = String(raw ?? '')
    .normalize('NFD')
    .replace(/\p{Diacritic}/gu, '')
    .trim()
    .toLowerCase()
  if (n === 'manana') return 'Mañana'
  if (n === 'tarde') return 'Tarde'
  if (n === 'noche' || n === 'nocturna') return 'Noche'
  return null
}

export function normalizarDocumento(valor: unknown) {
  if (valor === null || valor === undefined || valor === '') return ''
  if (typeof valor === 'number' && Number.isFinite(valor)) {
    return String(Math.trunc(valor))
  }
  return String(valor).trim().replace(/\s+/g, '')
}

export function normalizarEmail(valor: unknown) {
  if (valor === null || valor === undefined) return ''
  return String(valor).trim().toLowerCase()
}
