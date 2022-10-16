FROM python:3.8.4-slim-buster
COPY . usr/src/app
WORKDIR /usr/src/app
ENV FLASK_APP=app.py
ENV FLASK_RUN_HOST=0.0.0.0
#Server will reload itself on file changes if in dev mode
ENV FLASK_ENV=development
RUN python -m pip install --upgrade pip
RUN pip install -r requirements.txt
ENTRYPOINT flask RUN
