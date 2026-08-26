# SIGEVA front — lo que le pegas al agente de frontend

Este archivo **es el brief**. Las fotos, el Network y el checklist LISTO de Paula/Sofia viven en `documentacion/SIGEVA-Guia-Codigo-Eleccion-Global.docx` (mismas URLs, archivos reales de sigevaFront).

## Encargo (léelo tú, agente de frontend)

1. **Asigna**, no hagas las dos personas en un solo PR.
2. Abre **dos tareas** (o dos ramas) con los bloques de abajo, tal cual.
3. El equipo **ya tiene** React de producción: `sigevaFront` (carpeta hermana). **No copies** estas carpetas `pages/gestion`. Trabaja en los archivos que ya existen (tabla de abajo). No inventes URLs.
4. El back corre en `http://localhost:3333`. Vite proxea `/api`.
5. Grafía de jornada, siempre: `Mañana` | `Tarde` | `Noche` (con ñ). Nada de `manana`.

| Persona | Rama | Archivos reales (sigevaFront) | No toca |
|---|---|---|---|
| **Paula** | `feat/form-eleccion-global` | `FormEleccion.tsx`, `EleccionEditarModal.tsx`, `EleccionesActivasPage.tsx`, `EleccionDetalleModal.tsx` | Candidatos, urna |
| **Sofia** | `feat/tarjeton-jornada` | `AgregarCandidatoModal.tsx`, `ModificarCandidatoModal.tsx`, `GestionCandidatos.tsx`, `VotacionesActivasPage.tsx`, `VotacionCard.tsx`, `SeleccionarCandidatoPage.tsx` | Form crear/editar elección |

```bash
cd sigeva-front
npm i
npm run dev
```

---

## Reparte así (no mezcles)

| Persona | Rama | Toca | No toca |
|---|---|---|---|
| **Paula** | `feat/form-eleccion-global` | Form y listado de **elección** | Candidatos, urna, tarjetón |
| **Sofia** | `feat/tarjeton-jornada` | Form **candidato**, bloques, tarjetón urna | Form crear/editar elección |

Archivos compartidos (`src/api/types.ts`, `src/api/client.ts`, `src/constants/jornada.ts`, `src/App.tsx`, layouts): **no los reescribas**. Paula y Sofia solo entran a su carpeta de páginas y a su `api/eleccion.ts` o `api/candidatos.ts`.

```
src/pages/gestion/eleccion/      ← PAULA
src/api/eleccion.ts              ← PAULA
src/pages/gestion/candidatos/    ← SOFIA
src/pages/urna/                  ← SOFIA
src/api/candidatos.ts            ← SOFIA
```

Rutas del contrato:

- `/gestion/elecciones` — listado (Paula)
- `/gestion/elecciones/nueva` — POST crear (Paula)
- `/gestion/elecciones/:id/editar` — PUT (Paula)
- `/gestion/elecciones/:id/candidatos` — form + tres bloques (Sofia)
- `/urna` — tarjetón (Sofia)

---

## Pégale esto a Paula

**Título:** Form y listado de elección sin jornada  
**Rama:** `feat/form-eleccion-global`  
**Archivos:** `src/pages/gestion/eleccion/*` y `src/api/eleccion.ts`

Haces tres pantallas: listado, crear, editar. **No hay select de jornada.** El `idcentro_formacion` sale del funcionario logueado, no de un combo de sedes.

**POST** `/api/eleccion/crear` — body JSON (cambia el centro por el de la sesión):

```json
{
  "idcentro_formacion": 1,
  "nombre": "Representante de centro 2026",
  "fecha_inicio": "2026-09-01",
  "fecha_fin": "2026-09-05",
  "hora_inicio": "2026-09-01T08:00:00.000Z",
  "hora_fin": "2026-09-05T16:00:00.000Z"
}
```

Éxito: **201** `{ "message": "Eleccion creada con exito", "eleccion": { "jornada": null, ... } }`.  
Si el back aún responde **400** `"La jornada no es válida"`, tu form igual **no manda** `jornada`.

**PUT** `/api/eleccionActualizar/12` — **sí hay JSON**, mismos campos; puedes cambiar nombre o fechas. El `12` es el `ideleccion` del crear. Éxito: **200** `"Eleccion actualizada con exito"`.

```json
{
  "idcentro_formacion": 1,
  "nombre": "Representante de centro 2026 (horario ampliado)",
  "fecha_inicio": "2026-09-01",
  "fecha_fin": "2026-09-06",
  "hora_inicio": "2026-09-01T08:00:00.000Z",
  "hora_fin": "2026-09-06T18:00:00.000Z"
}
```

**GET listado** `/api/eleccionPorCentro/:idcentro` o `/api/eleccion/traerTodas/:idcentro`. La lista viene en `eleccionesActivas[]`. Cada item usa `titulo` (no `nombre`) y **no pintes** `jornada`. Una card por convocatoria.

**LISTO:** Network del crear = JSON de arriba y 201; del editar = JSON de arriba y 200; el form no tiene jornada; el listado es una card.

No toques candidatos ni urna.

---

## Pégale esto a Sofia

**Título:** Jornada en candidato + tarjetón filtrado  
**Rama:** `feat/tarjeton-jornada`  
**Archivos:** `src/pages/gestion/candidatos/*`, `src/pages/urna/*`, `src/api/candidatos.ts`

**Gestión — form** (pantalla que ya existe): agrega `<select required>` con exactamente `Mañana`, `Tarde`, `Noche`.

**POST** `/api/candidatos/crear` en **form-data** (no JSON puro):

```
ideleccion=12
idaprendiz=401
nombres=Ana Pérez
propuesta=Más bienestar en talleres
numero_tarjeton=01
jornada=Tarde
foto=(archivo jpg opcional)
```

Éxito: **201** `"Candidato registrado exitosamente"`. Tres altas, mismo tarjetón `01`, una jornada cada una. Si el segundo 01 falla, es el unique del back (Maicol), no tu form.

**GET gestión** `/api/candidatos/listar/:ideleccion` **sin** query → `data[]` con los tres. Agrupa en tres bloques.

**GET urna** `/api/candidatos/listar/:ideleccion?jornada=Tarde`. La jornada **no se pregunta**: sale del login del aprendiz.

```json
{
  "success": true,
  "data": {
    "id": 401,
    "jornada": "Tarde"
  }
}
```

Usa `data.jornada`. Si viene `null`, no armes modal “elige tu jornada”. Eso es otro paquete.

La urna muestra **una** elección del centro, no tres menús Mañana/Tarde/Noche. El recorte es de candidatos (`?jornada=`), no de convocar tres elecciones.

**LISTO:** Network del POST trae `jornada` en el FormData; gestión 3 bloques; urna llama `?jornada=` y solo ve esa franja.

No toques el form de crear elección.

---

## Lo que nadie hace

- Picker de jornada en el primer login del aprendiz.
- Acta / ganador por jornada.
- OTP, voto, import Excel.
- Renombrar URLs del back (`/api/eleccion/crear`, `/api/eleccionActualizar/:idEleccion`, `/api/candidatos/crear`, `/api/candidatos/listar/:ideleccion`).

Tipos canónicos (no cambien nombres de campos): `src/api/types.ts`.
