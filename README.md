# CinemaAPI

Backend-сервис для работы с фильмами: списки просмотра (watchlist), отзывы с рейтингами, лайки и аутентификация пользователей.

## Стек технологий

- **FastAPI** — веб-фреймворк
- **PostgreSQL** — база данных
- **SQLAlchemy 2.0 (async)** — ORM
- **Alembic** — миграции базы данных
- **JWT (access + refresh токены)** — аутентификация
- **Pydantic v2** — валидация данных
- **Docker / Docker Compose** — контейнеризация

## Возможности

- Регистрация и аутентификация пользователей через JWT (access + refresh токены)
- Просмотр каталога фильмов
- Личные watchlist'ы пользователей с поддержкой soft delete (удалённые записи не стираются физически, а помечаются как неактивные)
- Отзывы на фильмы с ограничением на диапазон рейтинга
- Лайки отзывов/фильмов

## Установка и запуск

### Через Docker Compose

```bash
git clone <ссылка-на-репозиторий>
cd cinemaapi
cp .env.example .env
docker-compose up --build
```

### Локально

```bash
git clone <ссылка-на-репозиторий>
cd cinemaapi
python -m venv venv
venv\Scripts\activate        # Windows
source venv/bin/activate     # Linux/Mac

pip install -r requirements.txt

# Применить миграции
alembic upgrade head

# Запустить сервер
uvicorn app.main:app --reload
```

## Переменные окружения

Создайте файл `.env` в корне проекта на основе `.env.example`:

```env
DATABASE_URL=postgresql+asyncpg://user:password@localhost:5432/cinemaapi
SECRET_KEY=your-secret-key
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=30
REFRESH_TOKEN_EXPIRE_DAYS=7
```

## Структура проекта

```
cinemaapi/
├── app/
│   ├── models/          # SQLAlchemy модели
│   ├── schemas/         # Pydantic схемы
│   ├── repositories/    # Repository pattern — доступ к данным
│   ├── routers/          # Эндпоинты FastAPI
│   ├── services/         # Бизнес-логика
│   ├── core/              # Конфигурация, безопасность (JWT)
│   └── main.py
├── alembic/               # Миграции базы данных
├── tests/
├── .env.example
├── docker-compose.yml
├── requirements.txt
└── README.md
```

## API документация

После запуска сервера документация Swagger доступна по адресу:

```
http://localhost:8000/docs
```

## Основные эндпоинты

### Аутентификация
| Метод | Путь | Описание |
|-------|------|----------|
| POST | `/auth/register` | Регистрация пользователя |
| POST | `/auth/login` | Вход, получение access/refresh токенов |
| POST | `/auth/refresh` | Обновление access токена |

### Фильмы
| Метод | Путь | Описание |
|-------|------|----------|
| GET | `/movies` | Список фильмов (с пагинацией) |
| GET | `/movies/{id}` | Информация о фильме |

### Watchlist
| Метод | Путь | Описание |
|-------|------|----------|
| GET | `/watchlist` | Получить watchlist пользователя |
| POST | `/watchlist` | Добавить фильм в watchlist |
| DELETE | `/watchlist/{id}` | Удалить из watchlist (soft delete) |

### Отзывы
| Метод | Путь | Описание |
|-------|------|----------|
| GET | `/movies/{id}/reviews` | Отзывы на фильм |
| POST | `/movies/{id}/reviews` | Оставить отзыв (рейтинг + текст) |
| POST | `/reviews/{id}/like` | Поставить лайк отзыву |

> Точные пути и параметры эндпоинтов уточните по фактической реализации в `app/routers/` — здесь приведена ориентировочная структура.

## Миграции

Создание новой миграции после изменения моделей:

```bash
alembic revision --autogenerate -m "описание изменений"
alembic upgrade head
```

## Автор

Александр — backend-разработчик (Python/FastAPI)
