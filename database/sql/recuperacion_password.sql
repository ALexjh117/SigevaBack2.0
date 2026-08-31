-- Recuperación de contraseña con OTP al correo (todos los roles).
-- Idempotente. Misma caducidad que el OTP de votación: OTP_EXPIRATION_MINUTES (default 5).
--
-- tipo = 'usuario'  → id_referencia = usuarios.idusuarios
--                     (Administrador, admin_sistema, Funcionario)
-- tipo = 'aprendiz' → id_referencia = aprendiz.idaprendiz

CREATE TABLE IF NOT EXISTS recuperacion_password (
  id SERIAL PRIMARY KEY,
  email VARCHAR(120) NOT NULL,
  codigo VARCHAR(32) NOT NULL,
  tipo VARCHAR(20) NOT NULL,
  id_referencia INTEGER NOT NULL,
  created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
  updated_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP
);

CREATE INDEX IF NOT EXISTS idx_recuperacion_password_email
  ON recuperacion_password (email);

CREATE INDEX IF NOT EXISTS idx_recuperacion_password_codigo
  ON recuperacion_password (codigo);
