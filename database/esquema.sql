-- ==========================================
-- CIMAGRAF - ESTRUCTURA DE BASE DE DATOS
-- Motor: SQLite
-- ==========================================

CREATE TABLE IF NOT EXISTS usuarios (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    usuario VARCHAR(40) NOT NULL UNIQUE,
    clave_hash TEXT NOT NULL,
    activo INTEGER NOT NULL DEFAULT 1 CHECK (activo IN (0, 1)),
    creado_en TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE IF NOT EXISTS ordenes (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    codigo VARCHAR(7) NOT NULL UNIQUE,
    maquina VARCHAR(4) NOT NULL,
    procesadas INTEGER NOT NULL CHECK (procesadas > 0),
    merma INTEGER NOT NULL CHECK (
        merma >= 0 AND merma <= procesadas
    ),
    inicio TEXT NOT NULL,
    fin TEXT NOT NULL CHECK (fin > inicio),
    creado_por INTEGER REFERENCES usuarios(id),
    creado_en TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP,
    actualizado_en TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP
);

CREATE INDEX IF NOT EXISTS idx_ordenes_maquina
ON ordenes(maquina);

CREATE INDEX IF NOT EXISTS idx_ordenes_merma
ON ordenes(merma, procesadas);

CREATE TABLE IF NOT EXISTS auditoria (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    usuario_id INTEGER REFERENCES usuarios(id),
    accion VARCHAR(20) NOT NULL,
    entidad VARCHAR(40) NOT NULL,
    entidad_id INTEGER,
    detalle TEXT NOT NULL DEFAULT '{}',
    fecha TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP
);

CREATE INDEX IF NOT EXISTS idx_auditoria_fecha
ON auditoria(fecha DESC);
