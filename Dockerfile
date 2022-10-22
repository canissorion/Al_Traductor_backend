#==========================================#
# Build stage 1: "python"                  #
# Base común para el resto de build stages #
#==========================================#
FROM python:3.10 as python

# Mostrar inmediatamente en consola las salidas stdout y stderr de Python.
ENV PYTHONUNBUFFERED=true
WORKDIR /app

#===============================================================#
# Build stage 2: "poetry"                                       #
# Instalación de poetry para gestionar el resto de dependencias #
#===============================================================#
FROM python as poetry

# Configuración de poetry.
ENV POETRY_HOME=/opt/poetry
ENV POETRY_VIRTUALENVS_IN_PROJECT=true
ENV PATH="$POETRY_HOME/bin:$PATH"

# Método de instalación de poetry recomendado,
# según https://python-poetry.org/docs/#installation.
RUN curl -sSL https://install.python-poetry.org | python3 -
COPY . ./
RUN poetry install --no-interaction --no-ansi -vvv

#=============================================================#
# Build stage 3: "runtime"                                    #
# Copia y configura el virtual environment del stage "poetry" #
# Levanta el servidor de la API                               #
#=============================================================#
FROM python as runtime
ENV PATH="/app/.venv/bin:$PATH"
COPY --from=poetry /app /app
EXPOSE 8000
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
