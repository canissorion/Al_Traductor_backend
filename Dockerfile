#==========================================#
# Build stage 1: "python"                  #
# Base común para el resto de build stages #
#==========================================#
FROM python:3.10-slim AS python

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

COPY . /app
RUN pip install -r requirements.txt

ENV PATH="/app/.venv/bin:$PATH"

EXPOSE 8000
CMD ["python3", "-m", "main"]
