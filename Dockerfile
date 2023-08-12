FROM python:3.11

RUN pip3 install --no-cache-dir pipenv

RUN mkdir /auth_app
WORKDIR /auth_app

COPY . .

RUN pipenv install --system --deploy

#RUN chmod a+x /auth_app/start.sh

RUN alembic upgrade head

CMD gunicorn app.main:app --workers 1 --worker-class uvicorn.workers.UvicornWorker --bind=0.0.0.0:8000
