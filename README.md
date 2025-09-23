# LogiXport - Sistema de Gestión Logística y Comercio Exterior

LogiXport es una aplicación web completa para la gestión de operaciones logísticas, exportación e importación, desarrollada con FastAPI y PostgreSQL. El sistema proporciona herramientas para el manejo de normativas, leyes y regulaciones relacionadas con el comercio internacional.

## Características Principales

- **Panel de Administración**: Gestión completa de usuarios, materiales didácticos y normativas
- **Banco de Datos Normativos**: Acceso a leyes, reglamentos y normativas de importación/exportación
- **Gestión de Usuarios**: Sistema de autenticación y autorización con diferentes roles
- **Material Didáctico**: Carga y gestión de documentos educativos sobre comercio exterior
- **Tarifas LIGIE**: Consulta de fracciones arancelarias y sus históricos
- **Diseño Responsivo**: Interfaz adaptable a dispositivos móviles y de escritorio
- **API RESTful**: Endpoints para integración con otros sistemas

## Estructura del Proyecto

```
LogiXport/
├── database_lzl/              # Módulo de conexión a base de datos
│   ├── __init__.py
│   ├── auth.py                # Funciones de autenticación
│   ├── db_connection.py       # Funciones de conexión a PostgreSQL
│   ├── db_models.py           # Modelos básicos y operaciones CRUD
│   ├── models_sqlalchemy.py   # Modelos SQLAlchemy para ORM
│   ├── inicializar_datos.py   # Scripts para inicializar datos
│   └── inicializar_tarifas.py # Scripts para inicializar tarifas
├── web_app/                   # Aplicación web
│   ├── middleware/            # Middleware de la aplicación
│   │   └── auth_middleware.py # Middleware de autenticación
│   ├── models/                # Modelos de datos para la API
│   │   └── auth_models.py     # Modelos de autenticación
│   ├── router/                # Enrutadores FastAPI
│   │   ├── admin_api.py       # API para administradores
│   │   ├── api_routes.py      # Rutas de API general
│   │   ├── auth_routes.py     # Rutas de autenticación
│   │   └── web_routes.py      # Rutas de páginas web
│   └── templates/             # Plantillas y recursos frontend
│       ├── pages/             # Páginas principales
│       ├── panel_admin/       # Páginas de administración
│       ├── sections/          # Secciones reutilizables
│       └── style/             # CSS y JavaScript
├── app.py                     # Punto de entrada de la aplicación
├── server.js                  # Servidor Node.js alternativo
└── requirements.txt           # Dependencias del proyecto
```

## Tecnologías Utilizadas

### Backend
- **FastAPI**: Framework web de alto rendimiento
- **SQLAlchemy**: ORM para interacción con la base de datos
- **Pydantic**: Validación de datos y serialización
- **JWT**: Autenticación basada en tokens
- **Jinja2**: Motor de plantillas

### Frontend
- **Tailwind CSS**: Framework CSS utilitario
- **JavaScript**: Interactividad del lado del cliente
- **Font Awesome**: Iconos vectoriales

### Base de Datos
- **PostgreSQL**: Sistema de gestión de base de datos relacional

## Requisitos

- Python 3.8 o superior
- PostgreSQL 12 o superior
- Node.js 14+ (opcional, para servidor alternativo)

## Instalación

1. Clonar el repositorio o descargar los archivos

2. Crear un entorno virtual e instalar dependencias:

```bash
python -m venv venv
venv\Scripts\activate  # En Windows
source venv/bin/activate  # En Linux/Mac
pip install -r requirements.txt
```

3. Configurar la base de datos PostgreSQL:
   - Crear una base de datos llamada `Db_LogiXport`
   - Asegurarse de que los parámetros de conexión en `database_lzl/db_connection.py` sean correctos

4. Inicializar datos básicos (opcional):

```bash
python -m database_lzl.inicializar_datos
python -m database_lzl.inicializar_tarifas
```

## Ejecución

### Usando FastAPI (recomendado)

Para iniciar la aplicación en modo desarrollo con recarga automática:

```bash
uvicorn app:app --reload --host 0.0.0.0 --port 8000
```

O simplemente:

```bash
python app.py
```

La aplicación estará disponible en http://localhost:8000

### Usando Node.js (alternativo)

```bash
node server.js
```

## Seguridad

Nota: En un entorno de producción, se recomienda:

1. Almacenar las credenciales de la base de datos en variables de entorno o un archivo .env
2. Implementar HTTPS
3. Configurar correctamente los mecanismos de autenticación y autorización
4. Cambiar la clave secreta para JWT en `database_lzl/auth.py`

## Desarrollo

Para contribuir al proyecto:

1. Crear una rama para la nueva funcionalidad
2. Implementar los cambios siguiendo las convenciones de código
3. Ejecutar pruebas (cuando estén disponibles)
4. Enviar un pull request