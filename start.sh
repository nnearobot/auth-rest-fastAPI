#!/bin/bash

# Start the database service
docker-compose up -d db

# Wait for the database service to start
sleep 10

alembic upgrade head

gunicorn app.main:app --workers 4 --worker-class uvicorn.workers.UvicornWorker --bind=0.0.0.0:8000