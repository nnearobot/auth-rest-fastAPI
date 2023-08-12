FROM python:3.11

RUN pip3 install --no-cache-dir pipenv

RUN mkdir /auth_app
WORKDIR /auth_app

COPY . .

RUN pipenv install --system --deploy

RUN chmod a+x /auth_app/start.sh
