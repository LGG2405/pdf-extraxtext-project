# pdf-extraxtext-project
Proyecto de desarrollo de software 2026. Ingenieria en Sistemas de la Informacion UTN FRSR.

## Tecnologias

- Python
- UV
- Modelo de IA (A definir)
- Ollama (a definir a futuro)
- xD
- Base de datos no relacional MongoDB

## Metodologías

- TDD
- Proyectos dirigidos en GitHub}
- Llos 6 primeros principios del 12 Factor App

## Principios de programación

- KISS
- DRY
- YAGNI
- SOLID

---

## 📁 Estructura del Proyecto (Arquitectura de Tres Capas)

```
.
├── app/
│   ├── main.py              # Punto de entrada de la aplicación
│   ├── core/                # Configuraciones centrales
│   │   ├── config.py        # Configuración con Pydantic Settings
│   │   ├── exceptions.py    # Excepciones de dominio
│   │   └── logging.py       # Configuración de logging
│   ├── db/                  # Capa de base de datos
│   │   └── database.py      # Configuración SQLAlchemy async
│   ├── models/              # Modelos ORM (Capa de Datos)
│   │   └── user.py
│   ├── schemas/             # Schemas Pydantic (Validación)
│   │   └── user.py
│   ├── repositories/        # Patrón Repository (Capa de Datos)
│   │   ├── base.py          # Repositorio base genérico
│   │   └── user_repository.py
│   ├── services/            # Lógica de negocio (Capa de Negocio)
│   │   └── user_service.py
│   ├── api/                 # Capa de Presentación
│   │   └── v1/
│   │       ├── router.py    # Router principal v1
│   │       └── endpoints/
│   │           └── users.py # Endpoints de usuarios
│   └── tests/               # Tests
├── pyproject.toml           # Configuración del proyecto (uv)
├── .env.example             # Ejemplo de variables de entorno
└── .gitignore
```

## 🏗️ Arquitectura de Tres Capas

### 1️⃣ Capa de Presentación (API)
- **Ubicación**: `app/api/`
- **Responsabilidad**: Recibir requests HTTP, validar entrada, delegar a servicios
- **Principios Clean Code**: Funciones pequeñas, nombres descriptivos, sin lógica de negocio

### 2️⃣ Capa de Negocio (Services)
- **Ubicación**: `app/services/`
- **Responsabilidad**: Implementar reglas de negocio, validaciones, coordinar operaciones
- **Principios Clean Code**: Una sola responsabilidad por servicio, métodos verbosos y descriptivos

### 3️⃣ Capa de Datos (Repositories)
- **Ubicación**: `app/repositories/`
- **Responsabilidad**: Acceso a base de datos, operaciones CRUD
- **Principios Clean Code**: Patrón Repository para desacoplamiento, repositorio base genérico

## 🚀 Iniciar el Proyecto con UV

### Requisitos previos
- Python 3.11 o superior
- UV instalado: `pip install uv`

### 1. Crear entorno virtual e instalar dependencias

```powershell
# UV crea automáticamente el entorno virtual e instala dependencias
uv sync
```

Para instalar también las dependencias de desarrollo:

```powershell
uv sync --dev
```

### 2. Configurar variables de entorno

```powershell
copy .env.example .env
```

Edita el archivo `.env` con tu configuración.

### 3. Ejecutar la aplicación

```powershell
uv run uvicorn app.main:app --reload
```

## 🛠️ Comandos UV útiles

```powershell
# Instalar dependencias
uv sync

# Instalar dependencias de desarrollo
uv sync --dev

# Agregar una dependencia
uv add fastapi

# Agregar dependencia de desarrollo
uv add --dev pytest

# Ejecutar comandos en el entorno
uv run python app/main.py

# Ejecutar tests
uv run pytest

# Formatear código con ruff
uv run ruff check .
uv run ruff format .

# Type checking con mypy
uv run mypy .
```

## 📚 Documentación de la API

Una vez iniciada la aplicación, accede a:

- **Swagger UI**: http://localhost:8000/docs
- **ReDoc**: http://localhost:8000/redoc
- **Health Check**: http://localhost:8000/health

## 🧪 Testing

```powershell
# Ejecutar todos los tests
uv run pytest

# Ejecutar con cobertura
uv run pytest --cov=app --cov-report=html
```
