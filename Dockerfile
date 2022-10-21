FROM python:3.10

# Instalar las dependencias por separado para que Docker pueda cachearlas.
WORKDIR /usr/src
COPY ./requirements.txt /usr/src/requirements.txt
RUN pip install --no-cache-dir --upgrade -r /usr/src/requirements.txt

# Copiar el código del servicio y desplegarlo en el servidor uvicorn.
COPY . /usr/src
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
