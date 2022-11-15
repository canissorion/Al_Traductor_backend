#==========================================#
# Build stage 1: "python"                  #
# Base común para el resto de build stages #
#==========================================#
FROM python:3.10 AS python

# Mostrar inmediatamente en consola las salidas stdout y stderr de Python.
ENV PYTHONUNBUFFERED=true
WORKDIR /app

#===============================================================#
# Build stage 2: "poetry"                                       #
# Instalación de poetry para gestionar el resto de dependencias #
#===============================================================#
FROM python AS poetry

# Configuración de poetry.
ENV POETRY_HOME=/opt/poetry
ENV PATH="$POETRY_HOME/bin:$PATH"

# Método recomendado de instalación de poetry,
# según https://python-poetry.org/docs/#installation.
RUN curl -sSL https://install.python-poetry.org | python3 -
COPY . /app
RUN poetry config virtualenvs.in-project true
RUN poetry install --no-interaction --no-ansi -vvv

#=============================================================#
# Build stage 3: "runtime"                                    #
# Copia y configura el virtual environment del stage "poetry" #
# Levanta el servidor de la API                               #
#=============================================================#
FROM python AS runtime

ENV PATH="/app/.venv/bin:$PATH"
COPY --from=poetry /app /app

EXPOSE 8000
CMD ["python", "-m", "main"]
