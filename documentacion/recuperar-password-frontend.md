> **Paquete para el compañero del front:** `para-companero/recuperar-password/` (README + JSON de cada API + Thunder). Este archivo es el mismo contrato, más corto.

# README — Recuperar contraseña (frontend)

**Repo:** `sigevaFront` (el React de producción, carpeta hermana de `sigevaBack`).  
**Back:** `http://localhost:3333` (Vite / axios usan `VITE_BASE_URL`).  
**Swagger:** `http://localhost:3333/docs` → tag **Recuperación de contraseña**.

El backend **ya está listo**. Tu trabajo es conectar la pantalla que ya existe. No inventes URLs. No preguntes el rol. No preguntes jornada.

---

## 1. Encargo (léelo entero)

Hoy el aprendiz o el funcionario entra a **Recuperar contraseña**, pone el **documento** y el front llama rutas que **el back no tiene**. Por eso no funciona.

Hay que cambiarlo al mismo patrón del OTP de votación:

1. El usuario escribe su **correo**.
2. El back manda un **código de 6 caracteres** a ese correo (caduca en 5 minutos).
3. El usuario escribe el código + la **nueva contraseña**.
4. El back cambia la clave. El front lo manda al **login que le toca** según el perfil que devolvió el API.

**Un solo flujo para los 4 roles:** Aprendiz, Funcionario, admin_sistema, Administrador.  
El front **no** pregunta “¿eres aprendiz o funcionario?”. Manda el email; el back busca en `usuarios` y en `aprendiz`.

---

## 2. Qué hay hoy (está mal) y qué debes dejar

| Archivo | Qué hace hoy | Qué debes hacer |
|---|---|---|
| `src/pages/RecuperarContrasena.tsx` | Pide **número de documento**. Llama `/api/usuarios/recuperar-contrasena` o `/api/aprendiz/recuperar-contrasena` (esas rutas **no existen**). Siempre muestra toast de éxito aunque falle. | Reescribir el form a **3 pasos** (correo → código+clave → listo). Llamar las 2 rutas de abajo. Pintar el `message` del back. **Mantén** el layout: `login-page`, foto, marcas SENA, `Login.css`. |
| `src/pages/Login.tsx` | Link a `/recuperar-contrasena?desde=aprendiz` o `?desde=funcionario`. | **No lo rompas.** El `?desde=` solo sirve para el botón “Volver al inicio”. No lo uses para elegir URL del API. |
| `src/App.tsx` | Ya tiene `<Route path="/recuperar-contrasena" element={<RecuperarContrasena />} />`. | **No agregues** otra ruta. Los 3 pasos van **en la misma página** (un `useState` de paso). |
| `src/api.ts` | Axios con `baseURL: VITE_BASE_URL`. | Reutilízalo. `api.post('/api/recuperar-password/solicitar', body)`. |

**No toques:** form de elección, candidatos, urna, OTP de voto (`/api/validaciones/...`), `auth.provider`, `types.ts` del back.

**Prohibido llamar:**

- `PUT /api/aprendiz/actualizar/contrasena` → el back responde **410**.
- `/api/usuarios/recuperar-contrasena`
- `/api/aprendiz/recuperar-contrasena`

---

## 3. Rutas del back (las únicas)

Base: `VITE_BASE_URL` + path. En local el path queda `/api/recuperar-password/...`.

| Paso | Método | Ruta | Cuándo |
|---|---|---|---|
| 1 | `POST` | `/api/recuperar-password/solicitar` | El usuario pulsa “Enviar código” |
| 2 | `POST` | `/api/recuperar-password/confirmar` | El usuario pulsa “Cambiar contraseña” |

Reenviar código = volver a llamar **solicitar** con el mismo email. El código anterior se invalida.

Content-Type: `application/json`. Sin token. Sin `x-user-id`.

---

## 4. Paso 1 — pedir el código

### Request

`POST /api/recuperar-password/solicitar`

```json
{
  "email": "alexchaguendo01@gmail.com"
}
```

| Campo | Tipo | Reglas |
|---|---|---|
| `email` | string | Obligatorio, formato email. Trim. |

**No mandes** `numero_documento`, `rol`, `perfil`, `jornada`, ni `desde`.

### Response 200

```json
{
  "success": true,
  "message": "Código enviado al correo",
  "data": {
    "otp_generado": true,
    "email_enviado_a": "alexchaguendo01@gmail.com",
    "email_enviado": true,
    "expira_en_minutos": 5
  }
}
```

En **desarrollo** el JSON trae además:

```json
{
  "codigo_otp_temporal": "T-RKAY",
  "_desarrollo_nota": "El código OTP se incluye solo en desarrollo. En producción, obtenerlo del email."
}
```

En producción **no** viene el código. El usuario lo saca del correo (asunto: `Código para recuperar tu contraseña - SIGEVA`).  
Puedes mostrar `codigo_otp_temporal` solo si existe (útil en local). No lo pidas como campo obligatorio de la UI.

### Errores paso 1

Axios tira en 400/404/500. Lee `error.response.data.message`.

| HTTP | `codigo_error` | `message` | Qué pintar |
|---|---|---|---|
| 404 | `CUENTA_NO_ENCONTRADA` | No hay una cuenta con ese correo | Ese texto. No pases al paso 2. |
| 400 | — | Datos de entrada inválidos | Correo mal formado. |
| 500 | `EMAIL_NO_ENVIADO` | No se pudo enviar el correo. Intenta de nuevo más tarde. | Toast de error. Reintentar. |
| 404 de **ruta** (HTML, no JSON) | — | — | El back viejo sigue en el 3333. Dile a backend que reinicie `node ace serve --hmr`. |

Ejemplo 404 de cuenta:

```json
{
  "success": false,
  "message": "No hay una cuenta con ese correo",
  "codigo_error": "CUENTA_NO_ENCONTRADA"
}
```

Si salió 200: guarda el email en state, pasa al **paso 2**, toast “Revisa tu correo. El código caduca en 5 minutos.”

---

## 5. Paso 2 — código + nueva clave

### Request

`POST /api/recuperar-password/confirmar`

```json
{
  "email": "alexchaguendo01@gmail.com",
  "codigo": "T-RKAY",
  "nueva_password": "NuevaClave2026"
}
```

| Campo | Tipo | Reglas |
|---|---|---|
| `email` | string | **El mismo** del paso 1. |
| `codigo` | string | Exactamente **6** caracteres. El back lo pasa a mayúsculas. `trim()` + `toUpperCase()` antes de mandar. Puede traer letras, números o un guion (nanoid). No valides solo `[A-Z0-9]`. |
| `nueva_password` | string | Mínimo **8**, máximo **72**. |

**No mandes** `confirmar_password`. Ese match es solo del form.

Validación en el front **antes** del POST:

- Código: `codigo.trim().length === 6`
- Clave: `nueva.length >= 8`
- Repetir clave: `nueva === repetir` (si no coinciden, no llames al API)

### Response 200

```json
{
  "success": true,
  "message": "Contraseña actualizada con éxito",
  "data": {
    "perfil": "Aprendiz",
    "login": "/api/aprendiz/login"
  }
}
```

`data.login` es la ruta **del API de login**, no la del React. Para navegar usá **`data.perfil`**:

| `data.perfil` (string exacto) | A dónde `navigate` |
|---|---|
| `Aprendiz` | `/login-aprendiz` |
| `Funcionario` | `/login` |
| `admin_sistema` | `/login` |
| `Administrador` | `/login` |

**No hagas login automático.** No llames a `login()` del auth. Toast de éxito + botón o redirect al login de esa tabla. La clave vieja ya no sirve; la nueva se prueba en esa pantalla.

Ignorá `?desde=` para este redirect. El perfil lo dice el back, no el link de origen. Un funcionario puede haber abierto la página desde el login de aprendiz.

### Errores paso 2

| HTTP | `codigo_error` | `message` | Qué pintar |
|---|---|---|---|
| 400 | `OTP_INVALIDO` | El código no es válido o ya fue usado | Código incorrecto. Quédate en el paso 2. |
| 400 | `OTP_EXPIRADO` | El código ya expiró. Solicita uno nuevo. | Botón **Reenviar código** (vuelve a `solicitar`). |
| 400 | — | Datos de entrada inválidos | Clave menor a 8 o código distinto de 6. |
| 404 | `CUENTA_NO_ENCONTRADA` | No hay una cuenta con ese correo | Raro (la cuenta se borró). Volver al paso 1. |

Después de un 200 el código **no se reutiliza**. Si el usuario confirma dos veces, la segunda es `OTP_INVALIDO`.

---

## 6. Cómo debe verse el flujo (misma URL)

Ruta React (ya existe): **`/recuperar-contrasena`**

Query opcional (ya la manda Login.tsx):

- `?desde=aprendiz` → el “Volver” apunta a `/login-aprendiz`
- `?desde=funcionario` → el “Volver” apunta a `/login`

```
paso = "email" | "codigo" | "exito"
```

### Paso `email`

- Título: Recuperar contraseña
- Texto: “Escribe el correo de tu cuenta. Te enviaremos un código de 6 caracteres.”
- Input: **Correo electrónico** (`type="email"`, `autoComplete="email"`)
- Botón: “Enviar código”
- Link: Volver al inicio (`volverA` según `desde`)
- **Sin** input de documento. **Sin** combo de rol. **Sin** jornada.

### Paso `codigo`

- Texto: “Enviamos el código a {email}. Caduca en {expira_en_minutos} minutos.”
- Input código (6, `autoComplete="one-time-code"`)
- Input nueva contraseña
- Input repetir contraseña
- Botón: “Cambiar contraseña”
- Link/botón: “Reenviar código” → `solicitar` otra vez
- Link: “Usar otro correo” → vuelve a `paso = "email"` (limpia código y claves)

### Paso `exito`

- Texto: “Contraseña actualizada.”
- Botón: “Iniciar sesión” → `/login-aprendiz` o `/login` según `perfil`

Reutilizá clases de `Login.css` (`login-page`, `login-card`, `login-panel`, `login-submit`, `login-error`, `login-devolver`). No armes otra marca visual.

---

## 7. Código para copiar (axios, como el resto del proyecto)

`src/api.ts` ya exporta `api`. En la página:

```ts
import axios from "axios";
import { api } from "../api";

function mensajeApi(error: unknown): string {
  if (axios.isAxiosError(error)) {
    const data = error.response?.data as { message?: string } | undefined;
    return data?.message || "No se pudo completar la solicitud";
  }
  return "No se pudo completar la solicitud";
}

type SolicitarOk = {
  success: boolean;
  message: string;
  data: {
    otp_generado: boolean;
    email_enviado_a: string;
    email_enviado: boolean;
    expira_en_minutos: number;
    codigo_otp_temporal?: string;
  };
};

type ConfirmarOk = {
  success: boolean;
  message: string;
  data: {
    perfil: "Aprendiz" | "Funcionario" | "admin_sistema" | "Administrador" | string;
    login: string;
  };
};

export async function solicitarRecuperacion(email: string) {
  const { data } = await api.post<SolicitarOk>("/api/recuperar-password/solicitar", {
    email,
  });
  return data;
}

export async function confirmarRecuperacion(payload: {
  email: string;
  codigo: string;
  nueva_password: string;
}) {
  const { data } = await api.post<ConfirmarOk>("/api/recuperar-password/confirmar", {
    email: payload.email,
    codigo: payload.codigo.trim().toUpperCase(),
    nueva_password: payload.nueva_password,
  });
  return data;
}

export function rutaLoginSegunPerfil(perfil: string) {
  return perfil === "Aprendiz" ? "/login-aprendiz" : "/login";
}
```

Puedes dejar esas funciones arriba de `RecuperarContrasena.tsx` o en `src/api/recuperarPassword.ts`. **No reescribas** `src/api.ts`.

En el submit, **no** envuelvas el error en un toast genérico de éxito (eso hace la página hoy). Si falla, `toast.error(mensajeApi(error))`.

---

## 8. Cómo probarlo (Network + Thunder)

Back levantado en **3333**. Front: `npm run dev` en `sigevaFront`.

### Thunder / fetch — solicitar

```
POST http://localhost:3333/api/recuperar-password/solicitar
Content-Type: application/json

{ "email": "alexchaguendo01@gmail.com" }
```

Esperas **200** y, en local, `data.codigo_otp_temporal`.

### Thunder — confirmar

```
POST http://localhost:3333/api/recuperar-password/confirmar
Content-Type: application/json

{
  "email": "alexchaguendo01@gmail.com",
  "codigo": "PEGAR_EL_CODIGO_DE_6",
  "nueva_password": "NuevaClave2026"
}
```

Esperas **200** y `data.perfil: "Aprendiz"` para ese correo.

### Desde la UI (F12 → Network)

1. Login aprendiz o funcionario → “Recuperar contraseña”.
2. URL: `/recuperar-contrasena?desde=...`
3. Escribes el correo → Network del **solicitar** = JSON de arriba, **200**.
4. Payload **solo** `{ "email": "..." }`.
5. Llega el mail (o usas `codigo_otp_temporal`).
6. Código + clave nueva (8+) + repetir → Network del **confirmar** = JSON de arriba, **200**.
7. Payload tiene `email`, `codigo`, `nueva_password`. Nada más.
8. Te manda a `/login-aprendiz` si era Aprendiz, a `/login` si era staff.
9. Entras con la **nueva** clave. La anterior falla.
10. Código inventado → **400** `OTP_INVALIDO`.
11. Esperas 6 min o pides otro código y usas el viejo → **400** `OTP_EXPIRADO` o inválido.
12. Correo que no existe → **404** y el mensaje en pantalla. **No** toast de “si está registrado…”.

---

## 9. LISTO

- [ ] Ya no se pide documento. Se pide **correo**.
- [ ] Network solicitar = `POST /api/recuperar-password/solicitar` + JSON `{ email }` + **200**.
- [ ] Network confirmar = `POST /api/recuperar-password/confirmar` + JSON `{ email, codigo, nueva_password }` + **200**.
- [ ] No aparece ninguna llamada a `/api/usuarios/recuperar-contrasena`, `/api/aprendiz/recuperar-contrasena` ni `PUT .../actualizar/contrasena`.
- [ ] No hay select de rol ni de jornada en esta pantalla.
- [ ] Código de 6. Clave mínimo 8. Las dos claves coinciden en el front.
- [ ] Reenviar código vuelve a llamar solicitar.
- [ ] Aprendiz termina en `/login-aprendiz`. Funcionario / admin_sistema / Administrador en `/login`.
- [ ] Login con la clave nueva funciona.
- [ ] 404 de correo y 400 de código se ven en la UI (toast o `login-error`).
- [ ] Layout sigue siendo el de `Login.css` (misma card, misma foto de recuperar).

---

## 10. Si algo no cuadra

| Síntoma | Causa |
|---|---|
| 404 con HTML / “Cannot GET” en la ruta nueva | Back viejo en el puerto 3333. Reiniciar Adonis. |
| 404 JSON `CUENTA_NO_ENCONTRADA` | Ese correo no está en `usuarios` ni en `aprendiz`. |
| 200 pero `email_enviado: false` | SMTP falló; en local igual viene `codigo_otp_temporal`. |
| El código del mail no entra | Caducó (5 min) o no son 6 caracteres. Reenviar. |
| Login no acepta la clave nueva | Confirmó mal el email, o estás en el login del rol contrario. |

El back **no** te va a crear otra ruta. Si el Network no coincide con este README, el front está llamando mal.
