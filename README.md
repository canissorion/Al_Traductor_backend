# AI Translator - Backend

[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)

Traductor de mapudungún, español e inglés, basado en modelos ML y servicios Cloud.

## I. Desarrollo en Docker

Para levantar el servicio en un contenedor de Docker:

```bash
docker-compose up --build
```

Las dependencias y configuraciones necesarias son gestionadas automáticamente
en el contenedor.

## II. Desarrollo local

### 1. Instalación de Poetry

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

### 2. Instalación de dependencias

Para instalar las dependencias de desarrollo y de ejecución del servicio:

```bash
poetry install
```

### 3. Despliegue

Para desplegar el servicio, levantar el servidor `uvicorn` en <http://localhost:31415>  y ejecutar el servicio:

```bash
uvicorn main:app --reload --host localhost --port 31415
```

> Si el contenedor Docker (ver sección [I. Desarrollo en Docker](#i-desarrollo-en-docker)) se está ejecutando, cambiar el puerto del comando anterior a uno disponible.

## III. Ejecución

### 1. Servicio API

Una vez desplegado, el servicio queda alojado en `http://localhost:31415`. Para
comprobar la conexión con el servicio, llamar al endpoint `connection`:

```bash
$ curl -H "Content-Type: application/json" -X GET http://localhost:31415/connection
{"status":"OK"}
```

### 2. Documentación

La documentación del servicio se genera automáticamente (mientras el servicio
esté levantado correctamente) en dos formatos: Swagger UI y ReDoc.

- Para acceder a la documentación provista por Swagger UI, entrar a
<http://localhost:31415/docs>.

- Para acceder a la documentación provista por ReDoc, entrar a
<http://localhost:31415/redoc>.

En ambos casos, la documentación se puede descargar en formato OpenAPI.
