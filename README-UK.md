# Orrin Backend

> 🇬🇧 [Read in English](README.md)

Бекенд **Orrin** — музичного стримінгового сервісу з функціями соціальної мережі, побудованого на Django REST Framework з підтримкою WebSocket через Django Channels та асинхронним транспортним шаром на Redis.

---

## Зміст

- [Огляд](#огляд)
- [Архітектура](#архітектура)
- [Технічний стек](#технічний-стек)
- [Запуск проекту](#запуск-проекту)
- [Автентифікація](#автентифікація)
- [API Довідник](#api-довідник)
- [WebSocket](#websocket)
- [Змінні середовища](#змінні-середовища)
- [Розгортання](#розгортання)
- [Адмін-панель](#адмін-панель)

---

## Огляд

Orrin дозволяє стримити музику, вести персональну бібліотеку треків і виконавців, ділитися враженнями через стрічку публікацій, спілкуватися в реальному часі та відстежувати активність друзів. Бекенд надає RESTful API для всіх клієнтських взаємодій, а WebSocket забезпечує реальний час для чату і push-сповіщень.

---

## Архітектура

Проект організований як незалежні Django-застосунки, кожен із яких відповідає за свою доменну область:

| Застосунок | Відповідальність |
|---|---|
| `orrin` | Треки, виконавці, жанри, альбоми, плейлисти, тексти пісень |
| `users` | Автентифікація, профілі, підписки, сповіщення |
| `library` | Вподобані треки, підписки на виконавців, історія прослуховувань, збережені альбоми |
| `feed` | Публікації, коментарі, реакції (лайки, репости, збереження), скарги |
| `chat` | Приватні повідомлення в реальному часі (WebSocket) |
| `stats` | Персональна статистика прослуховувань |
| `notes` | Нотатки користувачів до треків і виконавців |
| `legal` | Документи «Умови використання» та «Політика конфіденційності» |

---

## Технічний стек

| Шар | Технологія |
|---|---|
| Мова | Python 3.13 |
| Фреймворк | Django 5.2 + Django REST Framework |
| ASGI-сервер | Daphne |
| WebSockets | Django Channels + channels-redis |
| База даних | PostgreSQL 16 |
| Кеш / Брокер | Redis 7 |
| Автентифікація | Simple JWT (access + refresh токени), Google OAuth2 |
| Медіасховище | Cloudinary (зображення — тип `image`, аудіо — тип `raw`) |
| Статика | Whitenoise |
| Документація API | drf-spectacular (Swagger UI + ReDoc) |
| Аудіометадані | mutagen |
| Slug-генерація | python-slugify |
| Контейнеризація | Docker + Docker Compose |

---

## Запуск проекту

### Передумови

- [Docker](https://docs.docker.com/get-docker/) та [Docker Compose](https://docs.docker.com/compose/)

### Кроки

```bash
# 1. Клонуйте репозиторій
git clone <repo-url>
cd orrin-backend

# 2. Створіть файл змінних середовища
cp .env.example .env
# Заповніть необхідні значення у .env

# 3. Зберіть і запустіть контейнери
docker-compose up --build

# 4. Застосуйте міграції бази даних
docker-compose exec web python manage.py migrate

# 5. (Опційно) Створіть суперкористувача
docker-compose exec web python manage.py createsuperuser

# 6. (Опційно) Заповніть юридичні документи
docker-compose exec web python manage.py seed_legal_documents
```

| Сервіс | URL |
|---|---|
| API | `http://localhost:8000` |
| Swagger UI | `http://localhost:8000/api/v1/docs/schema/swagger-ui/` |
| ReDoc | `http://localhost:8000/api/v1/docs/schema/redoc/` |
| Django Admin | `http://localhost:8000/admin/` |

---

## Автентифікація

Усі захищені ендпоінти потребують **JWT Bearer**-токена в заголовку `Authorization`.

```
Authorization: Bearer <access_token>
```

| Ендпоінт | Метод | Опис |
|---|---|---|
| `/api/v1/auth/token/` | POST | Отримати access + refresh токен |
| `/api/v1/auth/token/refresh/` | POST | Оновити access токен |
| `/api/v1/auth/token/verify/` | POST | Перевірити дійсність токена |
| `/api/v1/auth/register/` | POST | Реєстрація нового користувача |
| `/api/v1/auth/google/login/` | POST | Вхід через Google OAuth2 |
| `/api/v1/auth/password/reset/` | POST | Запит на надсилання листа зі скиданням пароля |
| `/api/v1/auth/password/reset/confirm/` | POST | Підтвердження скидання пароля за токеном |

---

## API Довідник

### Треки

| Метод | Ендпоінт | Опис |
|---|---|---|
| GET | `/api/v1/tracks/` | Список треків — підтримує `search` та `ordering` |
| GET | `/api/v1/tracks/{slug}/` | Деталі треку з текстом пісні та статусом `is_liked` |
| POST | `/api/v1/tracks/{slug}/like/` | Додати / зняти лайк з треку |

### Виконавці

| Метод | Ендпоінт | Опис |
|---|---|---|
| GET | `/api/v1/artists/` | Список виконавців — підтримує `search` та `ordering` |
| GET | `/api/v1/artists/{slug}/` | Профіль виконавця: популярні треки, дискографія, учасники, схожі виконавці |
| POST | `/api/v1/artists/{slug}/follow/` | Підписатись / відписатись від виконавця |
| GET | `/api/v1/artists/{slug}/posts/` | Публікації менеджерів виконавця |
| GET | `/api/v1/artists/{slug}/notes/` | Публічні нотатки до виконавця |
| POST | `/api/v1/artists/{slug}/notes/` | Додати нотатку до виконавця |

### Альбоми

| Метод | Ендпоінт | Опис |
|---|---|---|
| GET | `/api/v1/library/albums/` | Збережені альбоми поточного користувача |
| POST | `/api/v1/library/albums/{slug}/save/` | Зберегти / прибрати зі збережених |

### Бібліотека

| Метод | Ендпоінт | Опис |
|---|---|---|
| GET | `/api/v1/library/` | Агрегований огляд: вподобані треки, підписки, плейлисти |
| GET | `/api/v1/library/liked/` | Усі вподобані треки |
| GET | `/api/v1/library/artists/` | Усі підписані виконавці |
| GET | `/api/v1/favorites/` | Псевдонім для `/api/v1/library/liked/` |

### Плейлисти

| Метод | Ендпоінт | Опис |
|---|---|---|
| GET, POST | `/api/v1/library/playlists/` | Список плейлистів / створення |
| GET, PATCH, DELETE | `/api/v1/library/playlists/{id}/` | Деталі / редагування / видалення |
| POST | `/api/v1/library/playlists/{id}/tracks/` | Додати трек (тіло: `track_slug`) |
| DELETE | `/api/v1/library/playlists/{id}/tracks/{slug}/` | Видалити трек |

### Історія прослуховувань

| Метод | Ендпоінт | Опис |
|---|---|---|
| GET, POST, DELETE | `/api/v1/history/` | Отримати / додати запис / очистити всю історію |
| DELETE | `/api/v1/history/{id}/` | Видалити окремий запис |

### Стрічка

| Метод | Ендпоінт | Опис |
|---|---|---|
| GET | `/api/v1/feed/` | Стрічка публікацій із фільтрами і пагінацією |
| POST | `/api/v1/feed/` | Створити публікацію (тіло: `text`, опційно `track_slug`) |
| GET, PATCH, DELETE | `/api/v1/feed/posts/{id}/` | Деталі / редагування / видалення |
| POST | `/api/v1/feed/posts/{id}/like/` | Лайк |
| POST | `/api/v1/feed/posts/{id}/repost/` | Репост |
| POST | `/api/v1/feed/posts/{id}/save/` | Збереження |
| POST | `/api/v1/feed/posts/{id}/report/` | Скарга |
| GET, POST | `/api/v1/feed/posts/{id}/comments/` | Список / додавання коментарів |

#### Параметри запиту стрічки

| Параметр | Значення | За замовчуванням |
|---|---|---|
| `feed_type` | `all`, `following` | `all` |
| `sort` | `recent`, `popular` | `recent` |
| `content_type` | `with_music`, `text_only`, _(без параметра — усі)_ | — |
| `page` | ціле число | `1` |

### Користувачі та соціальні функції

| Метод | Ендпоінт | Опис |
|---|---|---|
| GET, PATCH | `/api/v1/users/me/` | Власний профіль |
| GET | `/api/v1/users/{username}/` | Профіль будь-якого користувача |
| POST | `/api/v1/users/{username}/follow/` | Підписатись / відписатись |
| GET | `/api/v1/users/{username}/followers/` | Список підписників |
| GET | `/api/v1/users/{username}/following/` | Список підписок |
| GET | `/api/v1/users/{username}/posts/` | Публікації користувача |
| GET | `/api/v1/users/search/?search=` | Пошук користувачів |
| GET | `/api/v1/friends/activity/` | Нещодавно прослухані треки підписок |

### Нотатки

| Метод | Ендпоінт | Опис |
|---|---|---|
| GET, POST | `/api/v1/tracks/{slug}/notes/` | Нотатки до треку |
| GET, POST | `/api/v1/artists/{slug}/notes/` | Нотатки до виконавця |
| PATCH, DELETE | `/api/v1/notes/{id}/` | Редагування / видалення власної нотатки |
| POST | `/api/v1/notes/{id}/like/` | Лайк публічної нотатки |

### Чат

| Метод | Ендпоінт | Опис |
|---|---|---|
| GET, POST | `/api/v1/chats/` | Список чатів / створити або отримати чат |
| GET | `/api/v1/chats/{id}/` | Деталі чату |
| GET, POST | `/api/v1/chats/{id}/messages/` | Список повідомлень / відправити через REST |

### Статистика

| Метод | Ендпоінт | Опис |
|---|---|---|
| GET | `/api/v1/stats/top-tracks/` | Топ треків за особистою кількістю прослуховувань |
| GET | `/api/v1/stats/top-artists/` | Топ виконавців за особистою кількістю прослуховувань |
| GET | `/api/v1/stats/top-albums/` | Топ альбомів за особистою кількістю прослуховувань |

Усі ендпоінти статистики приймають опційний параметр `limit` (макс. 50, за замовч. 10).

### Сповіщення

| Метод | Ендпоінт | Опис |
|---|---|---|
| GET | `/api/notifications/` | Список усіх сповіщень |
| POST | `/api/notifications/{id}/read/` | Позначити сповіщення як прочитане |
| POST | `/api/notifications/read-all/` | Позначити всі сповіщення як прочитані |

### Юридичні документи

| Метод | Ендпоінт | Опис |
|---|---|---|
| GET | `/api/v1/legal/terms/` | Умови використання (`?lang=en` або `?lang=uk`) |
| GET | `/api/v1/legal/privacy/` | Політика конфіденційності (`?lang=en` або `?lang=uk`) |

---

## WebSocket

WebSocket-з'єднання потребує дійсного JWT access токена як query-параметра.

```
ws://host/ws/notifications/?token=<access_token>
ws://host/ws/chat/{chat_id}/?token=<access_token>
```

### Канал сповіщень

Сервер надсилає події автоматично; клієнту потрібно лише підтримувати з'єднання.

| Напрямок | Тип події | Опис |
|---|---|---|
| Сервер → Клієнт | `notification` | Нове сповіщення |

### Канал чату

| Напрямок | Тип події | Поля | Опис |
|---|---|---|---|
| Клієнт → Сервер | `send_message` | `text`, `trackId` | Надіслати повідомлення |
| Клієнт → Сервер | `typing_start` | — | Почати введення |
| Клієнт → Сервер | `typing_stop` | — | Зупинити введення |
| Сервер → Клієнт | `receive_message` | `id`, `chatId`, `senderId`, `text`, `trackId`, `timestamp`, `isRead` | Вхідне повідомлення |
| Сервер → Клієнт | `typing_start` | `senderId`, `chatId` | Інший учасник друкує |
| Сервер → Клієнт | `typing_stop` | `senderId`, `chatId` | Інший учасник зупинився |

---

## Змінні середовища

| Змінна | Обов'язкова | Опис |
|---|---|---|
| `SECRET_KEY` | ✅ | Django secret key |
| `POSTGRES_DB` | ✅ | Назва бази даних |
| `POSTGRES_USER` | ✅ | Користувач PostgreSQL |
| `POSTGRES_PASSWORD` | ✅ | Пароль PostgreSQL |
| `DB_HOST` | ✅ | Хост бази даних |
| `DB_PORT` | | Порт бази даних (за замовч. `5432`) |
| `GOOGLE_CLIENT_ID` | | Client ID для Google OAuth2 |
| `CLOUDINARY_CLOUD_NAME` | Prod | Ім'я хмари Cloudinary |
| `CLOUDINARY_API_KEY` | Prod | API-ключ Cloudinary |
| `CLOUDINARY_API_SECRET` | Prod | API-секрет Cloudinary |
| `DATABASE_URL` | Prod | Повний URL бази даних (замінює окремі DB-змінні) |
| `REDIS_URL` | Prod | URL підключення до Redis |
| `ALLOWED_HOSTS` | Prod | Дозволені хости через кому |
| `CORS_ALLOWED_ORIGINS` | Prod | Дозволені CORS-джерела через кому |
| `CSRF_TRUSTED_ORIGINS` | Prod | Довірені origins для CSRF через кому |
| `PASSWORD_RESET_FRONTEND_URL` | | Базовий URL фронтенду для листів зі скиданням пароля |
| `EMAIL_HOST_USER` | Prod | SMTP-логін (Gmail) |
| `EMAIL_HOST_PASSWORD` | Prod | SMTP-пароль (Gmail) |

---

## Розгортання

Проект постачається з `render.yaml` для розгортання на [Render](https://render.com) в один клік.

```bash
# Продакшн використовує модуль production-налаштувань
DJANGO_SETTINGS_MODULE=music_app.settings.production
```

Продакшн-конфігурація вмикає:

- `DEBUG=False` зі строгими `ALLOWED_HOSTS` та CORS-політикою
- PostgreSQL через `DATABASE_URL` з SSL
- Cloudinary для медіасховища (розумна маршрутизація: зображення → тип `image`, аудіо → тип `raw`)
- Redis channel layer для WebSocket
- Gmail SMTP для транзакційної пошти
- Whitenoise для роздачі статичних файлів

---

## Адмін-панель

Django admin доступний за адресою `/admin/` та надає повний CRUD для всіх сутностей, включно з:

- **Треки** — автоматичне визначення тривалості з аудіофайлу через mutagen
- **Виконавці** — управління складом гуртів, жанрами, менеджерами
- **Альбоми** — впорядковані треки через inline `AlbumTrack`
- **Плейлисти** — впорядковані треки через inline `PlaylistTrack`
- **Тексти пісень** — статичний звичайний текст або синхронізовані (karaoke-стиль) рядки
- **Стрічка** — публікації, коментарі, лайки, скарги
- **Чат** — історія повідомлень на кожну розмову
- **Користувачі** — управління профілями, граф підписників, статус верифікації
- **Сповіщення** — повний журнал сповіщень по користувачу
- **Юридичні документи** — управління «Умовами використання» та «Політикою конфіденційності» з підтримкою мов