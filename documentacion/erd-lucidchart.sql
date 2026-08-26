-- SIGEVA — ERD para Lucidchart
-- Lucidchart: File → Import → SQL → PostgreSQL → pegar este archivo.
-- Solo CREATE TABLE + FK. Sin ALTER. Sin CHECKs (el import suele fallar con ellos).

CREATE TABLE organizacion (
  idorganizacion INTEGER PRIMARY KEY,
  nombre VARCHAR(150) NOT NULL,
  slug VARCHAR(80) NOT NULL UNIQUE,
  tipo VARCHAR(40) NOT NULL,
  nit VARCHAR(20),
  estado VARCHAR(20) NOT NULL
);

CREATE TABLE perfil (
  idperfil INTEGER PRIMARY KEY,
  perfil VARCHAR(40) NOT NULL
);

CREATE TABLE regional (
  idregional INTEGER PRIMARY KEY,
  idorganizacion INTEGER NOT NULL,
  regional VARCHAR(120) NOT NULL,
  CONSTRAINT fk_regional_org FOREIGN KEY (idorganizacion) REFERENCES organizacion (idorganizacion)
);

CREATE TABLE centro_formacion (
  idcentro_formacion INTEGER PRIMARY KEY,
  idorganizacion INTEGER NOT NULL,
  idregional INTEGER,
  codigo_sede VARCHAR(20),
  centro_formacioncol VARCHAR(200) NOT NULL,
  direccion VARCHAR(200),
  telefono VARCHAR(50),
  correo VARCHAR(120),
  subdirector VARCHAR(120),
  correosubdirector VARCHAR(120),
  estado VARCHAR(20) NOT NULL,
  CONSTRAINT fk_centro_org FOREIGN KEY (idorganizacion) REFERENCES organizacion (idorganizacion),
  CONSTRAINT fk_centro_regional FOREIGN KEY (idregional) REFERENCES regional (idregional),
  CONSTRAINT uq_centro_codigo UNIQUE (idorganizacion, codigo_sede)
);

CREATE TABLE usuarios (
  idusuarios INTEGER PRIMARY KEY,
  idorganizacion INTEGER NOT NULL,
  idcentro_formacion INTEGER,
  idperfil INTEGER NOT NULL,
  nombres VARCHAR(80) NOT NULL,
  apellidos VARCHAR(80) NOT NULL,
  email VARCHAR(120) NOT NULL,
  password VARCHAR(255) NOT NULL,
  tipo_documento VARCHAR(20),
  numero_documento VARCHAR(20),
  celular VARCHAR(20),
  estado VARCHAR(20) NOT NULL,
  CONSTRAINT fk_usuarios_org FOREIGN KEY (idorganizacion) REFERENCES organizacion (idorganizacion),
  CONSTRAINT fk_usuarios_centro FOREIGN KEY (idcentro_formacion) REFERENCES centro_formacion (idcentro_formacion),
  CONSTRAINT fk_usuarios_perfil FOREIGN KEY (idperfil) REFERENCES perfil (idperfil),
  CONSTRAINT uq_usuarios_email UNIQUE (idorganizacion, email)
);

CREATE TABLE grupo (
  idgrupo INTEGER PRIMARY KEY,
  idorganizacion INTEGER NOT NULL,
  idcentro_formacion INTEGER NOT NULL,
  grupo VARCHAR(40) NOT NULL,
  jornada VARCHAR(20),
  CONSTRAINT fk_grupo_org FOREIGN KEY (idorganizacion) REFERENCES organizacion (idorganizacion),
  CONSTRAINT fk_grupo_centro FOREIGN KEY (idcentro_formacion) REFERENCES centro_formacion (idcentro_formacion)
);

CREATE TABLE votante (
  idvotante INTEGER PRIMARY KEY,
  idorganizacion INTEGER NOT NULL,
  idcentro_formacion INTEGER NOT NULL,
  idgrupo INTEGER,
  nombres VARCHAR(80) NOT NULL,
  apellidos VARCHAR(80) NOT NULL,
  email VARCHAR(120) NOT NULL,
  password VARCHAR(255),
  tipo_documento VARCHAR(20),
  numero_documento VARCHAR(20),
  celular VARCHAR(20),
  estado VARCHAR(40),
  CONSTRAINT fk_votante_org FOREIGN KEY (idorganizacion) REFERENCES organizacion (idorganizacion),
  CONSTRAINT fk_votante_centro FOREIGN KEY (idcentro_formacion) REFERENCES centro_formacion (idcentro_formacion),
  CONSTRAINT fk_votante_grupo FOREIGN KEY (idgrupo) REFERENCES grupo (idgrupo),
  CONSTRAINT uq_votante_email UNIQUE (idorganizacion, email)
);

CREATE TABLE elecciones (
  ideleccion INTEGER PRIMARY KEY,
  idorganizacion INTEGER NOT NULL,
  idcentro_formacion INTEGER NOT NULL,
  nombre VARCHAR(150) NOT NULL,
  jornada VARCHAR(20),
  fecha_inicio DATE NOT NULL,
  fecha_fin DATE NOT NULL,
  hora_inicio TIME NOT NULL,
  hora_fin TIME NOT NULL,
  CONSTRAINT fk_eleccion_org FOREIGN KEY (idorganizacion) REFERENCES organizacion (idorganizacion),
  CONSTRAINT fk_eleccion_centro FOREIGN KEY (idcentro_formacion) REFERENCES centro_formacion (idcentro_formacion)
);

CREATE TABLE candidatos (
  idcandidatos INTEGER PRIMARY KEY,
  idorganizacion INTEGER NOT NULL,
  ideleccion INTEGER NOT NULL,
  idvotante INTEGER NOT NULL,
  nombres VARCHAR(120),
  propuesta TEXT,
  foto VARCHAR(255),
  numero_tarjeton VARCHAR(10) NOT NULL,
  CONSTRAINT fk_cand_org FOREIGN KEY (idorganizacion) REFERENCES organizacion (idorganizacion),
  CONSTRAINT fk_cand_eleccion FOREIGN KEY (ideleccion) REFERENCES elecciones (ideleccion),
  CONSTRAINT fk_cand_votante FOREIGN KEY (idvotante) REFERENCES votante (idvotante),
  CONSTRAINT uq_tarjeton UNIQUE (ideleccion, numero_tarjeton),
  CONSTRAINT uq_votante_eleccion UNIQUE (ideleccion, idvotante)
);

CREATE TABLE validacion_voto (
  id INTEGER PRIMARY KEY,
  idorganizacion INTEGER NOT NULL,
  idvotante INTEGER NOT NULL,
  ideleccion INTEGER NOT NULL,
  codigo VARCHAR(6) NOT NULL,
  estado VARCHAR(20) NOT NULL,
  expira_en TIMESTAMP,
  CONSTRAINT fk_otp_org FOREIGN KEY (idorganizacion) REFERENCES organizacion (idorganizacion),
  CONSTRAINT fk_otp_votante FOREIGN KEY (idvotante) REFERENCES votante (idvotante),
  CONSTRAINT fk_otp_eleccion FOREIGN KEY (ideleccion) REFERENCES elecciones (ideleccion)
);

CREATE TABLE voto (
  idvoto INTEGER PRIMARY KEY,
  idorganizacion INTEGER NOT NULL,
  ideleccion INTEGER NOT NULL,
  idcandidatos INTEGER NOT NULL,
  idvotante INTEGER NOT NULL,
  CONSTRAINT fk_voto_org FOREIGN KEY (idorganizacion) REFERENCES organizacion (idorganizacion),
  CONSTRAINT fk_voto_eleccion FOREIGN KEY (ideleccion) REFERENCES elecciones (ideleccion),
  CONSTRAINT fk_voto_candidato FOREIGN KEY (idcandidatos) REFERENCES candidatos (idcandidatos),
  CONSTRAINT fk_voto_votante FOREIGN KEY (idvotante) REFERENCES votante (idvotante),
  CONSTRAINT uq_un_voto UNIQUE (idvotante, ideleccion)
);
