# AI Translator - Backend

[![Python: 3.10](https://img.shields.io/badge/python-3.10-blue.svg)](https://www.python.org/downloads/release/python-3100/)
[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)
[![Linter: pyright](https://img.shields.io/badge/linter-pyright-yellow.svg)](https://github.com/psf/black)

Traductor de mapudungún, español e inglés, basado en modelos ML y servicios Cloud.

## I. Despliegue en Docker

Para levantar el servicio en un contenedor de Docker usando Docker Compose:

```bash
docker-compose up --build
```

Las dependencias y configuraciones necesarias son gestionadas automáticamente
en el contenedor.

## II. Despliegue local

### 1. Requerimientos

- Python 3.10 o superior
- Poetry

### 2. Instalación de Poetry

El servicio utiliza Poetry como administrador de paquetes y dependencias. Para
instalarlo, ejecute uno de los siguientes comandos:

- Linux, macOS, Windows (WSL):

  ```bash
  curl -sSL https://install.python-poetry.org | python3 -
  ```

- Windows (Powershell):

  ```powershell
  (Invoke-WebRequest -Uri https://install.python-poetry.org -UseBasicParsing).Content | py -
  ```

Para más información, visitar la [documentación oficial de Poetry](https://python-poetry.org/docs/).

### 3. Instalación de dependencias

Para instalar las dependencias de desarrollo y de ejecución del servicio:

```bash
poetry install
```

### 4. Despliegue

Para desplegar el servicio, levantar el servidor `uvicorn` en <http://localhost:31415>  y ejecutar el servicio:

```bash
poetry run uvicorn main:app --reload --host localhost --port 31415
```

> Si el contenedor Docker (ver sección [I. Despliegue en Docker](#i-despliegue-en-docker)) se está ejecutando, cambiar el puerto del comando anterior a uno disponible.

## III. Ejecución

### 1. Servicio API

Una vez desplegado, el servicio queda alojado en `http://localhost:31415`. Para
comprobar la conexión con el servicio, llamar al endpoint `connection`:

```bash
curl -H "Content-Type: application/json" -X GET http://localhost:31415/connection
```

### 2. Documentación

La documentación del servicio se genera automáticamente (mientras el servicio
esté levantado correctamente) en dos formatos: Swagger UI y ReDoc.

- Para acceder a la documentación provista por Swagger UI, entrar a
<http://localhost:31415/docs>.

- Para acceder a la documentación provista por ReDoc, entrar a
<http://localhost:31415/redoc>.

En ambos casos, la documentación se puede descargar en formato OpenAPI.

### 3. Logs

`[TODO]`

## IV. Estructura

El servicio está construido en base a *Clean Architecture* [[1]](#1), y su
estructura se desprende en las siguientes carpetas:

- `api`: Capa de interfaces, que contiene los controladores, y sus
  respectivas definiciones de endpoints, requests, responses y puertos de
  entrada y salida.

- `core/kernel`: Clases abstractas de los componentes del núcleo del servicio.

- `core/domain`: Capas de entidades (o modelos de datos), de **casos**
  de uso (o features) y la capa intermedia de repositorios (fuentes de datos
  remotas o locales) y validadores.

- `infrastructure`: Drivers de la capa de infraestructura.

- `utils`: Funciones de utilidad del servicio.

A cada archivo del proyecto se le adjunta como sufijo su correspondiente tipo,
según la capa a la que pertenece: `feature`, `repository`, `source`,
`controller`, `request`, `response`, entre otros. Excepción a esta regla son
las entidades, que llevan solo el nombre que las identifica.

Notar que la capa de infraestructura está compuesta por los drivers, frameworks
y herramientas que integran el servicio. La carpeta `infrastructure` incluye
sólo los drivers; las configuraciones del framework web FastAPI y del resto de
herramientas, como las de Poetry y Docker, se encuentra en la raíz del
proyecto.

## V. Desarrollo

### 1. Dependencias

- Para agregar dependencias requeridas para la ejecución del servicio:

```bash
poetry add scipy
```

- Para agregar dependencias requeridas sólo para el desarrollo del servicio:

```bash
poetry add mypy --group dev
```

- Para eliminar una dependencia:

```bash
poetry remove tensorflow
```

### 2. Pruebas

`[TODO]`

## VI. Referencias

<a id="1">[1]</a>
Martin, R. C., Grenning, J., & Brown, S. (2018).
*Clean architecture: A craftsman's guide to software structure and Design.*
Prentice Hall.
