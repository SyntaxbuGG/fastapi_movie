set -o errexit

alembic upgrade head

gunicorn app.main:app --bind 0.0.0.0:$PORT --worker-class uvicorn.workers.UvicornWorker
