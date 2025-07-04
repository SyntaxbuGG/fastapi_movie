# 🎬 Moviestra FastAPI

![Build](https://github.com/SyntaxbuGG/moviestra_fastapi/actions/workflows/deploy.yml/badge.svg)
![License](https://img.shields.io/github/license/SyntaxbuGG/moviestra_fastapi)
![Python](https://img.shields.io/badge/python-3.13.2+-blue)

**Moviestra** — это backend-сервис для потокового кинотеатра, реализованный на FastAPI. Поддерживает регистрацию пользователей, просмотр фильмов, рейтинги, избранное, уровни подписки (`free`, `premium`, `vip`) и административные функции.

## 🚀 Возможности

* Регистрация / Аутентификация пользователей
* Уровни подписки и доступ к контенту (free / premium / vip)
* Добавление фильмов, описаний, жанров, тегов
* Рейтинги, лайки/дизлайки фильмов
* Избранное
* Админ-интерфейс
* Swagger/OpenAPI документация

## 🛠️ Технологии

* Python 3.13.2
* FastAPI
* SQLModel (based on SQLAlchemy)
* Alembic (DB migrations)
* PostgreSQL / SQLite
* Uvicorn
* Pydantic
* JWT Auth
* CORS, Logging, DI
* Docker
* GitHub Actions (CI)

## 📁 Структура проекта

```
moviestra_fastapi/
├── app/
│   ├── account/        # Модели и роуты пользователей
│   ├── movie/          # Модели и роуты фильмов
│   ├── core/           # Настройки, зависимости, конфиги
│   ├── common/         # Утилиты, общие схемы
│   └── main.py         # Точка входа
├── alembic/            # Миграции
├── .env                # Окружение
├── requirements.txt    # Зависимости
├── Dockerfile
├── docker-compose.yml
├── .github/
│   └── workflows/
│       └── deploy.yml      # CI pipeline
└── README.md
```

## ⚙️ Установка и запуск вручную

1. **Клонируйте репозиторий:**

```bash
git clone https://github.com/ваш-юзер/moviestra_fastapi.git
cd moviestra_fastapi
```

2. **Создайте виртуальное окружение:**

```bash
python -m venv venv
source venv/bin/activate  # Linux/macOS
venv\Scripts\activate     # Windows
```

3. **Установите зависимости:**

```bash
pip install -r requirements.txt
```

4. **Создайте `.env`:**

```env
DATABASE_URL= postgresql+asyncpg://.../..
# SECRET_KEY is used to sign and verify JWT tokens.
SECRET_KEY=your-secret-key
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=30
REFRESH_TOKEN_EXPIRE_DAYS=7

```

5. **Миграции:**

```bash
alembic upgrade head
```

6. **Запустите сервер:**

```bash
uvicorn app.main:app --reload
```

## 🐳 Запуск с Docker

1. **Создайте `.env` файл (как выше).**

2. **Соберите и запустите контейнеры:**

```bash
docker-compose up --build
```

3. **API будет доступно по адресу:**

```
http://localhost:8080
```

🔁 CI/CD (GitHub Actions)

Автоматические проверки, тесты и деплой на Render выполняются через GitHub Actions. Подробнее см. deploy.yml.

📜 start.sh

Скрипт start.sh выполняет миграции и запускает FastAPI-приложение через uvicorn. Используется при запуске в Docker и в CI/CD. Подробнее см. start.sh.

## 📚 API документация

* Swagger: [http://localhost:8000/docs](http://localhost:8000/docs)
* ReDoc: [http://localhost:8000/redoc](http://localhost:8000/redoc)

## 🔍 TODO / Планы

* Загрузка видео / обложек
* Рекомендации
* Оплаты Stripe / UZUM
* FastAPI-Admin / TortoiseAdmin

## 📄 Лицензия

MIT License

---

> Автор: [SyntaxBugg](https://github.com/SyntaxBugg)
