CREATE TABLE IF NOT EXISTS usuarios (
    id BIGSERIAL PRIMARY KEY,
    usuario VARCHAR(40) NOT NULL UNIQUE,
    clave_hash TEXT NOT NULL,
    activo BOOLEAN NOT NULL DEFAULT TRUE,
    creado_en TIMESTAMPTZ NOT NULL DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE IF NOT EXISTS ordenes (
    id BIGSERIAL PRIMARY KEY,
    codigo VARCHAR(7) NOT NULL UNIQUE,
    maquina VARCHAR(4) NOT NULL,
    procesadas INTEGER NOT NULL CHECK (procesadas > 0),
    merma INTEGER NOT NULL CHECK (merma >= 0 AND merma <= procesadas),
    inicio TIMESTAMP NOT NULL,
    fin TIMESTAMP NOT NULL CHECK (fin > inicio),
    creado_por BIGINT REFERENCES usuarios(id),
    creado_en TIMESTAMPTZ NOT NULL DEFAULT CURRENT_TIMESTAMP,
    actualizado_en TIMESTAMPTZ NOT NULL DEFAULT CURRENT_TIMESTAMP
);
CREATE INDEX IF NOT EXISTS idx_ordenes_maquina ON ordenes(maquina);
CREATE INDEX IF NOT EXISTS idx_ordenes_merma ON ordenes(merma, procesadas);

CREATE TABLE IF NOT EXISTS auditoria (
    id BIGSERIAL PRIMARY KEY,
    usuario_id BIGINT REFERENCES usuarios(id),
    accion VARCHAR(20) NOT NULL,
    entidad VARCHAR(40) NOT NULL,
    entidad_id BIGINT,
    detalle JSONB NOT NULL DEFAULT '{}'::jsonb,
    fecha TIMESTAMPTZ NOT NULL DEFAULT CURRENT_TIMESTAMP
);
CREATE INDEX IF NOT EXISTS idx_auditoria_fecha ON auditoria(fecha DESC);
