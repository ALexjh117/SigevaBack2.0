import { Navigate, Route, Routes } from 'react-router-dom'
import GestionShell from '@/layouts/GestionShell'
import UrnaShell from '@/layouts/UrnaShell'
import HomePage from '@/pages/HomePage'
import EleccionesListPage from '@/pages/gestion/eleccion/EleccionesListPage'
import EleccionFormPage from '@/pages/gestion/eleccion/EleccionFormPage'
import CandidatosGestionPage from '@/pages/gestion/candidatos/CandidatosGestionPage'
import TarjetonPage from '@/pages/urna/TarjetonPage'

export default function App() {
  return (
    <Routes>
      <Route path="/" element={<HomePage />} />
      <Route path="/gestion" element={<GestionShell />}>
        <Route index element={<Navigate to="elecciones" replace />} />
        <Route path="elecciones" element={<EleccionesListPage />} />
        <Route path="elecciones/nueva" element={<EleccionFormPage />} />
        <Route path="elecciones/:id/editar" element={<EleccionFormPage />} />
        <Route path="elecciones/:id/candidatos" element={<CandidatosGestionPage />} />
      </Route>
      <Route path="/urna" element={<UrnaShell />}>
        <Route index element={<TarjetonPage />} />
      </Route>
    </Routes>
  )
}
