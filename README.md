
# Cimagraf – Sistema de control de producción

Sistema académico modular desarrollado en Python y PostgreSQL para gestionar órdenes de producción, calcular unidades buenas, merma y duración, consultar registros, generar reportes y mantener una auditoría de cambios.

## 1. Requisitos
- Python 3.10 o superior.
- PostgreSQL 15 o superior.
- Git.

## 2. Instalación en Windows

```powershell
py -m venv .venv
.venv\Scripts\Activate.ps1
py -m pip install -r requirements.txt
```

Crea una base de datos llamada `cimagraf` en PostgreSQL.

Copia `.env.example` como `.env` y configura la conexión:

```text
DATABASE_URL=postgresql://postgres:TU_CLAVE@localhost:5432/cimagraf
```

No compartas ni subas el archivo `.env` a GitHub.

## 3. Inicialización

```powershell
py -m database.inicializar
```

Este proceso crea las tablas y permite registrar el primer usuario.

## 4. Ejecución

```powershell
py main.py
```

## 5. Pruebas

```powershell
py -m unittest discover -s tests -v
```

## 6. Arquitectura modular

- `views/`: presentación e interacción con el usuario.
- `controllers/`: coordinación de las operaciones.
- `services/`: validaciones, cálculos, autenticación, ordenamiento, auditoría y exportaciones.
- `models/`: estructuras de datos.
- `config/`: configuración de conexión.
- `database/`: esquema e inicialización de PostgreSQL.
- `tests/`: pruebas automatizadas.

El sistema utiliza una arquitectura de tres capas: presentación, lógica de negocio y datos.

## 7. Características principales

- Registro, consulta, modificación y eliminación de órdenes.
- Validación de códigos, máquinas, cantidades y fechas.
- Cálculo de unidades buenas, merma y duración.
- Búsqueda mediante código único e índices de PostgreSQL.
- Ordenamiento eficiente mediante `sorted()`.
- Resumen de producción por máquina.
- Autenticación con contraseñas protegidas mediante PBKDF2-HMAC-SHA256.
- Auditoría de operaciones.
- Exportación de reportes a CSV, JSON, TXT, BIN y PDF.

## 8. Flujo de trabajo Git

Ramas del proyecto:

- `main`: versión estable.
- `desarrollo`: integración del equipo.
- `modulo-base-datos`: trabajo relacionado con la base de datos.
- `modulo-aplicacion`: desarrollo de la aplicación.
- `modulo-reportes`: reportes y exportaciones.

Cada integrante debe trabajar en su rama, realizar commits y proponer la integración de sus cambios hacia `desarrollo`. Después de revisar y probar el proyecto, se integrará la versión final en `main`.

## 9. Consideraciones

Este proyecto es un prototipo académico. Para su uso real se requieren pruebas de integración, configuración segura, copias de seguridad y controles adicionales de acceso.

La información de ejemplo debe reemplazarse por datos reales verificados y autorizados.

---

**Repositorio:** Cimagraf-Control-Produccion  
**Tecnologías:** Python, PostgreSQL y Git/GitHub.
