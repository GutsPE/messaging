# Python-arch-main

## Descripción

Este proyecto implementa una arquitectura limpia para la gestión de mensajes utilizando FastAPI, SQLAlchemy y Pydantic. Permite crear, consultar y listar mensajes almacenados en una base de datos relacional, siguiendo buenas prácticas de separación de capas, pruebas automatizadas y despliegue en contenedores.

## Estructura del Proyecto

- **app/**: Código fuente principal.
  - **domain/**: Entidades y repositorios de dominio.
  - **application/**: Casos de uso (servicios de aplicación).
  - **infrastructure/**: Implementaciones concretas de repositorios, modelos ORM, esquemas y handlers de API.
  - **settings.py**: Configuración de la aplicación FastAPI.
  - **main.py**: Punto de entrada de la aplicación.
- **test/**: Pruebas unitarias y de integración.
  - **integration/**: Pruebas integrales (end-to-end) de la API.
- **requirements.txt**: Dependencias del proyecto.
- **.dockerignore**: Archivos y carpetas excluidos del contexto de Docker.
- **Dockerfile**: (Si existe) Para construir la imagen Docker de la aplicación.

## Instalación

1. Clona el repositorio y navega a la carpeta `Python-arch-main`.
2. Crea un entorno virtual:
   ```sh
   python -m venv venv
   venv\Scripts\activate  # En Windows
   ```
3. Instala las dependencias:
   ```sh
   pip install -r app/requirements.txt
   ```

## Uso

1. Configura las variables de entorno necesarias para la base de datos en un archivo `.env`.
2. Ejecuta la aplicación:
   ```sh
   cd app
   uvicorn main:app --reload --port 8000
   ```
3. Accede a la documentación interactiva en [http://localhost:8000/docs](http://localhost:8000/docs).

## Pruebas

Ejecuta los tests con pytest:
```sh
pytest
```

### Pruebas integrales

Las pruebas integrales se encuentran en `test/integration/test_messages.py` y cubren:

- Creación de mensajes (incluyendo validaciones y errores)
- Consulta de mensajes por ID
- Listado de todos los mensajes
- Listado de mensajes por sesión

Ejemplo de ejecución:
```sh
pytest test/integration/test_messages.py
```

### Medición de cobertura

Para medir la cobertura de los tests unitarios utiliza `pytest-cov`:

1. Instala la dependencia si no la tienes:
   ```sh
   pip install pytest-cov
   ```
2. Ejecuta:
   ```sh
   pytest --cov=app
   ```
   Para un reporte HTML:
   ```sh
   pytest --cov=app --cov-report=html
   ```
   El reporte se genera en la carpeta `htmlcov`. Abre `htmlcov/index.html` para ver el detalle.

**Cobertura actual:**  
- Cobertura total: **74%** (ver detalles en `htmlcov/index.html`)

## Docker

Si deseas construir y ejecutar la aplicación en un contenedor Docker:

1. Asegúrate de tener un `Dockerfile` en la raíz del proyecto.
2. Construye la imagen:
   ```sh
   docker build -t python-arch-main .
   ```
3. Ejecuta el contenedor:
   ```sh
   docker run -d -p 8000:8000 --env-file .env python-arch-main
   ```

El archivo `.dockerignore` excluye archivos temporales, entornos virtuales y carpetas de control de versiones para optimizar la construcción de la imagen.

## Endpoints principales

- `GET /messages/`: Lista todos los mensajes.
- `POST /messages/`: Crea un nuevo mensaje.
- `GET /messages/{message_id}`: Obtiene un mensaje por ID.
- `GET /messages/sessions/{session_id}`: Lista mensajes por sesión (con paginación y filtro por remitente).

## Autores

- Equipo de desarrollo (Giancarlo Villanueva Andrade)

## Licencia

Este proyecto está bajo la licencia