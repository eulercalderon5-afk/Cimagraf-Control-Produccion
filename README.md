 HEAD
# Cimagraf – Sistema de control de producción

Prototipo académico modular en Python con PostgreSQL. Gestiona órdenes, calcula unidades buenas, merma y duración, permite consultar/modificar/eliminar, registra auditoría y exporta reportes.

> Los datos de ejemplo son simulados para pruebas. No representan mediciones reales de Cimagraf salvo que el equipo los reemplace por datos verificados y autorizados.

## 1. Requisitos
- Python 3.10 o superior.
- PostgreSQL 15 o superior (también puede utilizarse una versión compatible más reciente).
- Git.

## 2. Preparar el proyecto en Windows
Abre la carpeta del proyecto en Visual Studio Code o abre una terminal dentro de ella.

```powershell
py -m venv .venv
.venv\Scripts\Activate.ps1
py -m pip install -r requirements.txt
```

Si PowerShell bloquea la activación, puedes ejecutar directamente `.venv\Scripts\python.exe` y `.venv\Scripts\pip.exe` sin cambiar políticas del sistema.

Crea una base de datos vacía llamada `cimagraf` desde pgAdmin o psql. Copia `.env.example` como `.env` y reemplaza `TU_CLAVE` por la contraseña local del usuario PostgreSQL:

```text
DATABASE_URL=postgresql://postgres:TU_CLAVE@localhost:5432/cimagraf
```

No subas `.env` a GitHub. Está excluido mediante `.gitignore`.

## 3. Crear tablas y primer usuario

```powershell
py -m database.inicializar
```

El programa crea las tablas, índices y solicita crear el primer usuario. La contraseña se almacena con PBKDF2-HMAC-SHA256 y una sal aleatoria; no se guarda en texto plano.

## 4. Ejecutar

```powershell
py main.py
```

## 5. Pruebas automáticas

```powershell
py -m unittest discover -s tests -v
```

Las pruebas de servicios no requieren conexión a PostgreSQL. Para validar el sistema completo, también se debe probar el inicio de sesión y las operaciones CRUD contra una base PostgreSQL local.

## 6. Arquitectura
- `views/`: entrada y presentación en consola.
- `controllers/`: casos de uso y coordinación de operaciones.
- `services/`: validaciones, cálculos, autenticación, ordenamiento, auditoría y exportación.
- `models/`: estructura de los datos.
- `config/`: conexión a PostgreSQL.
- `database/`: esquema e inicialización.
- `tests/`: pruebas automatizadas.

La solución utiliza una arquitectura de tres capas: presentación, lógica de negocio y datos. Los controladores separan los casos de uso de las pantallas y del acceso a datos.

## 7. Decisiones técnicas
- PostgreSQL es la base relacional principal. Las restricciones `CHECK`, claves únicas e índices apoyan la integridad y las consultas.
- La búsqueda por código usa una columna `UNIQUE`, respaldada por un índice de PostgreSQL.
- El ordenamiento en memoria utiliza `sorted()` (Timsort); no se implementan burbuja, selección ni inserción.
- El resumen por máquina usa un diccionario de acumulación, evitando búsquedas repetidas en listas.
- La auditoría registra usuario, acción, entidad, identificador, detalle y fecha.
- Exportaciones disponibles: CSV, JSON, TXT, BIN (formato binario propio con firma `CIM1`) y PDF.
- La contraseña se procesa con PBKDF2-HMAC-SHA256.

## 8. Formato de orden
- Código: `CIM-001` (se admiten códigos con más dígitos).
- Máquina: `M-01`.
- Fecha: `AAAA-MM-DD HH:MM`.
- Restricciones: procesadas > 0; 0 <= merma <= procesadas; fin > inicio.

## 9. Flujo Git recomendado para un equipo
Ramas: `main` (entrega estable), `desarrollo` (integración), `modulo-base-datos`, `modulo-aplicacion` y `modulo-reportes`.

Cada integrante trabaja en su rama, realiza commits con cambios reales y abre una solicitud de incorporación hacia `desarrollo`. Se revisa y prueba antes de fusionar. Al cerrar el proyecto, `desarrollo` se integra en `main`.

## 10. Limitaciones y mejoras futuras
Es un prototipo de consola académico. Para un despliegue real se necesitarían, entre otros, gestión de roles/permisos, recuperación de contraseña, política de copias de seguridad, configuración segura de secretos, pruebas de integración automatizadas y una interfaz gráfica/web. El PDF requiere la dependencia ReportLab instalada.

# Cimagraf-Control-Produccion
Sistema modular para el control de órdenes de producción, registro de merma, tiempos de máquina, auditoría y exportación de información.
 4f9e6dd2fff0b91499505df50ef5f2017ba45494
