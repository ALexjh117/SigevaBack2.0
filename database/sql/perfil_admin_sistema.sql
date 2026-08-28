-- HU-S2-030 — catálogo cerrado de 4 perfiles. Idempotente.
-- Los únicos roles: Administrador | Funcionario | Aprendiz | admin_sistema
-- No se inserta un quinto ni se duplica admin_sistema.
--
-- Usuario demo QA (centro = el de menor id):
--   correo:    admin.centro@sigeva.test
--   password:  AdminCentro2026
-- Login de gestión: POST /api/usuarios/login

INSERT INTO perfil (idperfil, perfil)
SELECT COALESCE((SELECT MAX(idperfil) FROM perfil), 0) + 1, 'admin_sistema'
WHERE NOT EXISTS (
  SELECT 1 FROM perfil WHERE perfil = 'admin_sistema'
);

CREATE UNIQUE INDEX IF NOT EXISTS uq_perfil_nombre ON perfil (perfil);

DO $$
DECLARE
  pid integer;
BEGIN
  SELECT idperfil INTO pid FROM perfil WHERE perfil = 'admin_sistema';
  IF pid IS NOT NULL THEN
    EXECUTE format(
      'CREATE UNIQUE INDEX IF NOT EXISTS uq_un_admin_sistema_por_centro ON usuarios (idcentro_formacion) WHERE idperfil = %s',
      pid
    );
  END IF;
END $$;

INSERT INTO usuarios (
  nombres,
  apellidos,
  celular,
  tipo_documento,
  numero_documento,
  email,
  password,
  estado,
  idperfil,
  idcentro_formacion
)
SELECT
  'Admin',
  'Centro',
  '3000000000',
  'CC',
  '99000001',
  'admin.centro@sigeva.test',
  '$2b$10$ZdL6xpUK5Yyf0c1nBpUmGut1PjeYoFOw8ptIn0sbYiXOTAOmjXQYu',
  'Activo',
  p.idperfil,
  c.idcentro_formacion
FROM perfil p
CROSS JOIN LATERAL (
  SELECT idcentro_formacion
  FROM centro_formacion
  ORDER BY idcentro_formacion
  LIMIT 1
) c
WHERE p.perfil = 'admin_sistema'
  AND NOT EXISTS (
    SELECT 1 FROM usuarios WHERE email = 'admin.centro@sigeva.test'
  );
