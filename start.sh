set -o errexit

alembic upgrade head

uvicorn app.main:app --bind 0.0.0.0:$PORT 
