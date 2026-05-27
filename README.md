# Orrin Backend

**[Українська](README.md)** | [English](README-ENG.md)

Бекенд частина веб-додатку **Orrin** — музичного сервісу з елементами соціальної мережі.

## 📋 Опис проекту

Orrin — це веб-додаток, що поєднує функціонал музичного стримінгового сервісу та соціальної мережі. Користувачі можуть слухати музику, вести персональну бібліотеку треків і виконавців, ділитися враженнями через стрічку публікацій, спілкуватися в реальному часі та відстежувати активність друзів.

Бекенд побудований на **Django REST Framework** з підтримкою WebSocket-з'єднань через **Django Channels** та асинхронним транспортним шаром на базі **Redis**.

---

## 🏗️ Архітектура

Проект розбитий на незалежні Django-застосунки за доменами:

| Застосунок | Відповідальність |
|---|---|
| `orrin` | Треки, виконавці, жанри, плейлисти |
| `users` | Автентифікація, профілі, підписки, сповіщення |
| `library` | Вподобані треки, підписки на виконавців, історія прослуховувань |
| `feed` | Публікації, коментарі, реакції (лайки, репости, збереження) |
| `chat` | Приватні повідомлення між користувачами (WebSocket) |
| `stats` | Персональна статистика прослуховувань |

---

## ⚙️ Технічний стек

- **Python 3.13** / **Django 5.2**
- **Django REST Framework** — REST API
- **Django Channels** + **Daphne** — ASGI-сервер, WebSocket-підтримка
- **channels-redis** — channel layer для Channels
- **PostgreSQL 16** — основна реляційна база даних
- **Redis 7** — брокер повідомлень для WebSocket та Channels
- **Simple JWT** — JWT-автентифікація (access + refresh токени)
- **Google OAuth2** — вхід через Google-акаунт
- **drf-spectacular** — автоматична генерація OpenAPI-схеми (Swagger / ReDoc)
- **mutagen** — розбір метаданих аудіофайлів (тривалість треку)
- **python-slugify** — генерація slug-ідентифікаторів

---

## 🚀 Запуск проекту

### Передумови

- Docker та Docker Compose

### Кроки

```bash
# 1. Клонуйте репозиторій
git clone <repo-url>
cd orrin-backend

# 2. Створіть .env на основі прикладу
cp .env.example .env

# 3. Запустіть контейнери
docker-compose up --build

# 4. Застосуйте міграції
docker-compose exec web python manage.py migrate

# 5. (Опційно) Створіть суперкористувача
docker-compose exec web python manage.py createsuperuser
```

Сервер буде доступний за адресою: `http://localhost:8000`  
Документація API (Swagger): `http://localhost:8000/api/v1/docs/schema/swagger-ui/`

---

## 🔑 Автентифікація

Усі захищені ендпоінти використовують **JWT Bearer**-токени.

| Ендпоінт | Метод | Опис |
|---|---|---|
| `/api/v1/auth/token/` | POST | Отримати access + refresh токен |
| `/api/v1/auth/token/refresh/` | POST | Оновити access токен |
| `/api/v1/auth/register/` | POST | Реєстрація нового користувача |
| `/api/v1/auth/google/login/` | POST | Вхід через Google OAuth2 |
| `/api/v1/auth/password/reset/` | POST | Запит на скидання пароля |
| `/api/v1/auth/password/reset/confirm/` | POST | Підтвердження скидання пароля |

---

## 📡 API — основні групи ендпоінтів

### Треки та виконавці
- `GET /api/v1/tracks/` — список треків із пошуком і сортуванням
- `GET /api/v1/tracks/{slug}/` — деталі треку
- `GET /api/v1/artists/` — список виконавців
- `GET /api/v1/artists/{slug}/` — профіль виконавця з популярними треками та схожими артистами

### Бібліотека
- `GET /api/v1/library/` — агрегований огляд: вподобані треки, підписки, плейлисти
- `GET /api/v1/library/liked/` — вподобані треки
- `POST /api/v1/tracks/{slug}/like/` — додати / зняти лайк з треку
- `GET /api/v1/library/artists/` — підписані виконавці
- `POST /api/v1/artists/{slug}/follow/` — підписатись / відписатись від виконавця
- `GET/POST/DELETE /api/v1/history/` — управління історією прослуховувань

### Плейлисти
- `GET/POST /api/v1/library/playlists/` — список плейлистів / створення
- `GET/PATCH/DELETE /api/v1/library/playlists/{id}/` — деталі, редагування, видалення
- `POST /api/v1/library/playlists/{id}/tracks/` — додати трек
- `DELETE /api/v1/library/playlists/{id}/tracks/{slug}/` — видалити трек

### Стрічка
- `GET /api/v1/feed/` — стрічка публікацій із фільтрацією (`feed_type`, `sort`, `content_type`) та пагінацією
- `POST /api/v1/feed/` — створити публікацію
- `GET/PATCH/DELETE /api/v1/feed/posts/{id}/` — деталі, редагування, видалення
- `POST /api/v1/feed/posts/{id}/like/` — лайк
- `POST /api/v1/feed/posts/{id}/repost/` — репост
- `POST /api/v1/feed/posts/{id}/save/` — збереження
- `GET/POST /api/v1/feed/posts/{id}/comments/` — коментарі

### Користувачі та соціальні функції
- `GET/PATCH /api/v1/users/me/` — власний профіль
- `GET /api/v1/users/{username}/` — профіль будь-якого користувача
- `POST /api/v1/users/{username}/follow/` — підписатись / відписатись
- `GET /api/v1/users/{username}/followers/` — підписники
- `GET /api/v1/users/{username}/following/` — підписки
- `GET /api/v1/users/search/?search=` — пошук користувачів
- `GET /api/v1/friends/activity/` — активність підписок (нещодавно прослухані треки)

### Чат
- `GET/POST /api/v1/chats/` — список чатів / створення чату
- `GET /api/v1/chats/{id}/` — деталі чату
- `GET/POST /api/v1/chats/{id}/messages/` — повідомлення чату

### Статистика
- `GET /api/v1/stats/top-tracks/` — топ треків за кількістю прослуховувань
- `GET /api/v1/stats/top-artists/` — топ виконавців
- `GET /api/v1/stats/top-albums/` — топ за albumplay-статистикою

---

## 🔌 WebSocket

Підключення потребує JWT-токена як query-параметра.

| URL | Призначення |
|---|---|
| `ws://host/ws/notifications/?token=<access>` | Push-сповіщення для користувача |
| `ws://host/ws/chat/{chat_id}/?token=<access>` | Повідомлення чату в реальному часі |

**Події чату (клієнт → сервер):**
- `send_message` — надіслати повідомлення (поля: `text`, `trackId`)
- `typing_start` / `typing_stop` — індикатор введення

**Події чату (сервер → клієнт):**
- `receive_message` — нове повідомлення
- `typing_start` / `typing_stop` — індикатор введення від іншого учасника

---

## 🗂️ Змінні середовища

| Змінна | Опис |
|---|---|
| `SECRET_KEY` | Django secret key |
| `POSTGRES_DB` | Назва бази даних |
| `POSTGRES_USER` | Користувач PostgreSQL |
| `POSTGRES_PASSWORD` | Пароль PostgreSQL |
| `DB_HOST` | Хост бази даних |
| `DB_PORT` | Порт бази даних (за замовчуванням 5432) |
| `GOOGLE_CLIENT_ID` | Client ID для Google OAuth2 |
| `ALLOWED_HOSTS` | Дозволені хости (для production, через кому) |
| `CORS_ALLOWED_ORIGINS` | Дозволені CORS-джерела (для production, через кому) |
| `PASSWORD_RESET_FRONTEND_URL` | URL фронтенду для посилань скидання пароля |

---

## 🛠️ Адмін-панель

Django admin доступний за адресою `/admin/`. Підтримує:

- Управління треками з автоматичним розрахунком тривалості з аудіофайлу
- Управління виконавцями: склад гуртів, жанри, менеджери
- Перегляд та модерацію будь-яких сутностей проекту