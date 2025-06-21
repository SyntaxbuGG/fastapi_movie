set -o errexit

echo "🔄 Running Alembic migrations..."
alembic upgrade head

echo "🚀 Starting FastAPI app with Gunicorn..."
gunicorn app.main:app --workers 1 --worker-class uvicorn.workers.UvicornWorker --bind 0.0.0.0:${PORT:-8000}

