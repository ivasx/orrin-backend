# Orrin Backend

> 🇺🇦 [Читати українською](README-UK.md)

Backend for **Orrin** — a music streaming platform with social networking features, built with Django REST Framework,
WebSocket support via Django Channels, and an async transport layer powered by Redis.

---

## Table of Contents

- [Overview](#overview)
- [Architecture](#architecture)
- [Tech Stack](#tech-stack)
- [Getting Started](#getting-started)
- [Authentication](#authentication)
- [API Reference](#api-reference)
- [WebSocket](#websocket)
- [Environment Variables](#environment-variables)
- [Deployment](#deployment)
- [Admin Panel](#admin-panel)

---

## Overview

Orrin lets users stream music, maintain a personal library of tracks and artists, share thoughts through a social feed,
chat in real time, and track friends' listening activity. The backend exposes a RESTful API for all client interactions,
with real-time capabilities via WebSocket for chat and push notifications.

---

## Architecture

The project is organized as independent Django applications, each owning a distinct domain:

| App       | Responsibility                                                  |
|-----------|-----------------------------------------------------------------|
| `orrin`   | Tracks, artists, genres, albums, playlists, lyrics              |
| `users`   | Authentication, profiles, follows, notifications                |
| `library` | Liked tracks, followed artists, listening history, saved albums |
| `feed`    | Posts, comments, reactions (likes, reposts, saves), reports     |
| `chat`    | Real-time private messaging (WebSocket)                         |
| `stats`   | Personal listening statistics                                   |
| `notes`   | User annotations on tracks and artists                          |
| `legal`   | Terms of Service and Privacy Policy documents                   |

---

## Tech Stack

| Layer            | Technology                                                     |
|------------------|----------------------------------------------------------------|
| Language         | Python 3.13                                                    |
| Framework        | Django 5.2 + Django REST Framework                             |
| ASGI Server      | Daphne                                                         |
| WebSockets       | Django Channels + channels-redis                               |
| Database         | PostgreSQL 16                                                  |
| Cache / Broker   | Redis 7                                                        |
| Auth             | Simple JWT (access + refresh tokens), Google OAuth2            |
| Media Storage    | Cloudinary (images via `image` resource type, audio via `raw`) |
| Static Files     | Whitenoise                                                     |
| API Docs         | drf-spectacular (Swagger UI + ReDoc)                           |
| Audio Metadata   | mutagen                                                        |
| Slug Generation  | python-slugify                                                 |
| Containerization | Docker + Docker Compose                                        |

---

## Getting Started

### Prerequisites

- [Docker](https://docs.docker.com/get-docker/) and [Docker Compose](https://docs.docker.com/compose/)

### Setup

```bash
# 1. Clone the repository
git clone <repo-url>
cd orrin-backend

# 2. Create your environment file
cp .env.example .env
# Fill in the required values in .env

# 3. Build and start containers
docker-compose up --build

# 4. Apply database migrations
docker-compose exec web python manage.py migrate

# 5. (Optional) Create a superuser
docker-compose exec web python manage.py createsuperuser

# 6. (Optional) Seed legal documents
docker-compose exec web python manage.py seed_legal_documents
```

| Service      | URL                                                    |
|--------------|--------------------------------------------------------|
| API          | `http://localhost:8000`                                |
| Swagger UI   | `http://localhost:8000/api/v1/docs/schema/swagger-ui/` |
| ReDoc        | `http://localhost:8000/api/v1/docs/schema/redoc/`      |
| Django Admin | `http://localhost:8000/admin/`                         |

---

## Authentication

All protected endpoints require a **JWT Bearer** token in the `Authorization` header.

```
Authorization: Bearer <access_token>
```

| Endpoint                               | Method | Description                       |
|----------------------------------------|--------|-----------------------------------|
| `/api/v1/auth/token/`                  | POST   | Obtain access + refresh token     |
| `/api/v1/auth/token/refresh/`          | POST   | Refresh access token              |
| `/api/v1/auth/token/verify/`           | POST   | Verify token validity             |
| `/api/v1/auth/register/`               | POST   | Register a new user               |
| `/api/v1/auth/google/login/`           | POST   | Sign in with Google OAuth2        |
| `/api/v1/auth/password/reset/`         | POST   | Request password reset email      |
| `/api/v1/auth/password/reset/confirm/` | POST   | Confirm password reset with token |

---

## API Reference

### Tracks

| Method | Endpoint                      | Description                                    |
|--------|-------------------------------|------------------------------------------------|
| GET    | `/api/v1/tracks/`             | List tracks — supports `search` and `ordering` |
| GET    | `/api/v1/tracks/{slug}/`      | Track detail with lyrics and `is_liked` status |
| POST   | `/api/v1/tracks/{slug}/like/` | Toggle like on a track                         |

### Artists

| Method | Endpoint                         | Description                                                                   |
|--------|----------------------------------|-------------------------------------------------------------------------------|
| GET    | `/api/v1/artists/`               | List artists — supports `search` and `ordering`                               |
| GET    | `/api/v1/artists/{slug}/`        | Artist profile with popular tracks, discography, members, and similar artists |
| POST   | `/api/v1/artists/{slug}/follow/` | Toggle follow on an artist                                                    |
| GET    | `/api/v1/artists/{slug}/posts/`  | Posts authored by the artist's managers                                       |
| GET    | `/api/v1/artists/{slug}/notes/`  | Public notes attached to an artist                                            |
| POST   | `/api/v1/artists/{slug}/notes/`  | Create a note on an artist                                                    |

### Albums

| Method | Endpoint                              | Description                       |
|--------|---------------------------------------|-----------------------------------|
| GET    | `/api/v1/library/albums/`             | Saved albums for the current user |
| POST   | `/api/v1/library/albums/{slug}/save/` | Toggle save on an album           |

### Library

| Method | Endpoint                   | Description                                                    |
|--------|----------------------------|----------------------------------------------------------------|
| GET    | `/api/v1/library/`         | Aggregated overview: liked tracks, followed artists, playlists |
| GET    | `/api/v1/library/liked/`   | All liked tracks                                               |
| GET    | `/api/v1/library/artists/` | All followed artists                                           |
| GET    | `/api/v1/favorites/`       | Alias for `/api/v1/library/liked/`                             |

### Playlists

| Method             | Endpoint                                        | Description                        |
|--------------------|-------------------------------------------------|------------------------------------|
| GET, POST          | `/api/v1/library/playlists/`                    | List playlists / create a playlist |
| GET, PATCH, DELETE | `/api/v1/library/playlists/{id}/`               | Playlist detail / edit / delete    |
| POST               | `/api/v1/library/playlists/{id}/tracks/`        | Add a track (body: `track_slug`)   |
| DELETE             | `/api/v1/library/playlists/{id}/tracks/{slug}/` | Remove a track                     |

### Listening History

| Method            | Endpoint                | Description                         |
|-------------------|-------------------------|-------------------------------------|
| GET, POST, DELETE | `/api/v1/history/`      | Get history / add entry / clear all |
| DELETE            | `/api/v1/history/{id}/` | Remove a single entry               |

### Feed

| Method             | Endpoint                            | Description                                                               |
|--------------------|-------------------------------------|---------------------------------------------------------------------------|
| GET                | `/api/v1/feed/`                     | Post feed with `feed_type`, `sort`, `content_type` filters and pagination |
| POST               | `/api/v1/feed/`                     | Create a post (body: `text`, optional `track_slug`)                       |
| GET, PATCH, DELETE | `/api/v1/feed/posts/{id}/`          | Post detail / edit / delete                                               |
| POST               | `/api/v1/feed/posts/{id}/like/`     | Toggle like                                                               |
| POST               | `/api/v1/feed/posts/{id}/repost/`   | Toggle repost                                                             |
| POST               | `/api/v1/feed/posts/{id}/save/`     | Toggle save                                                               |
| POST               | `/api/v1/feed/posts/{id}/report/`   | Report a post                                                             |
| GET, POST          | `/api/v1/feed/posts/{id}/comments/` | List / add comments                                                       |

#### Feed query parameters

| Parameter      | Values                                      | Default  |
|----------------|---------------------------------------------|----------|
| `feed_type`    | `all`, `following`                          | `all`    |
| `sort`         | `recent`, `popular`                         | `recent` |
| `content_type` | `with_music`, `text_only`, _(omit for all)_ | —        |
| `page`         | integer                                     | `1`      |

### Users & Social

| Method     | Endpoint                              | Description                                 |
|------------|---------------------------------------|---------------------------------------------|
| GET, PATCH | `/api/v1/users/me/`                   | Own profile                                 |
| GET        | `/api/v1/users/{username}/`           | Any user's profile                          |
| POST       | `/api/v1/users/{username}/follow/`    | Toggle follow                               |
| GET        | `/api/v1/users/{username}/followers/` | Follower list                               |
| GET        | `/api/v1/users/{username}/following/` | Following list                              |
| GET        | `/api/v1/users/{username}/posts/`     | Posts by user                               |
| GET        | `/api/v1/users/search/?search=`       | User search                                 |
| GET        | `/api/v1/friends/activity/`           | Recent tracks listened to by followed users |

### Notes

| Method        | Endpoint                        | Description                  |
|---------------|---------------------------------|------------------------------|
| GET, POST     | `/api/v1/tracks/{slug}/notes/`  | Notes on a track             |
| GET, POST     | `/api/v1/artists/{slug}/notes/` | Notes on an artist           |
| PATCH, DELETE | `/api/v1/notes/{id}/`           | Edit / delete own note       |
| POST          | `/api/v1/notes/{id}/like/`      | Toggle like on a public note |

### Chat

| Method    | Endpoint                       | Description                             |
|-----------|--------------------------------|-----------------------------------------|
| GET, POST | `/api/v1/chats/`               | List chats / create or retrieve a chat  |
| GET       | `/api/v1/chats/{id}/`          | Chat detail                             |
| GET, POST | `/api/v1/chats/{id}/messages/` | List messages / send a message via REST |

### Statistics

| Method | Endpoint                     | Description                        |
|--------|------------------------------|------------------------------------|
| GET    | `/api/v1/stats/top-tracks/`  | Top tracks by personal play count  |
| GET    | `/api/v1/stats/top-artists/` | Top artists by personal play count |
| GET    | `/api/v1/stats/top-albums/`  | Top albums by personal play count  |

All stats endpoints accept an optional `limit` query parameter (max 50, default 10).

### Notifications

| Method | Endpoint                        | Description                    |
|--------|---------------------------------|--------------------------------|
| GET    | `/api/notifications/`           | List all notifications         |
| POST   | `/api/notifications/{id}/read/` | Mark a notification as read    |
| POST   | `/api/notifications/read-all/`  | Mark all notifications as read |

### Legal

| Method | Endpoint                 | Description                                 |
|--------|--------------------------|---------------------------------------------|
| GET    | `/api/v1/legal/terms/`   | Terms of Service (`?lang=en` or `?lang=uk`) |
| GET    | `/api/v1/legal/privacy/` | Privacy Policy (`?lang=en` or `?lang=uk`)   |

---

## WebSocket

WebSocket connections require a valid JWT access token passed as a query parameter.

```
ws://host/ws/notifications/?token=<access_token>
ws://host/ws/chat/{chat_id}/?token=<access_token>
```

### Notifications channel

The server pushes events automatically; the client only needs to maintain the connection.

| Direction       | Event type     | Description              |
|-----------------|----------------|--------------------------|
| Server → Client | `notification` | New notification payload |

### Chat channel

| Direction       | Event type        | Payload fields                                                       | Description                      |
|-----------------|-------------------|----------------------------------------------------------------------|----------------------------------|
| Client → Server | `send_message`    | `text`, `trackId`                                                    | Send a new message               |
| Client → Server | `typing_start`    | —                                                                    | Signal typing started            |
| Client → Server | `typing_stop`     | —                                                                    | Signal typing stopped            |
| Server → Client | `receive_message` | `id`, `chatId`, `senderId`, `text`, `trackId`, `timestamp`, `isRead` | Incoming message                 |
| Server → Client | `typing_start`    | `senderId`, `chatId`                                                 | Other participant is typing      |
| Server → Client | `typing_stop`     | `senderId`, `chatId`                                                 | Other participant stopped typing |

---

## Environment Variables

| Variable                      | Required | Description                                      |
|-------------------------------|----------|--------------------------------------------------|
| `SECRET_KEY`                  | ✅        | Django secret key                                |
| `POSTGRES_DB`                 | ✅        | Database name                                    |
| `POSTGRES_USER`               | ✅        | PostgreSQL username                              |
| `POSTGRES_PASSWORD`           | ✅        | PostgreSQL password                              |
| `DB_HOST`                     | ✅        | Database host                                    |
| `DB_PORT`                     |          | Database port (default `5432`)                   |
| `GOOGLE_CLIENT_ID`            |          | Client ID for Google OAuth2                      |
| `CLOUDINARY_CLOUD_NAME`       | Prod     | Cloudinary cloud name                            |
| `CLOUDINARY_API_KEY`          | Prod     | Cloudinary API key                               |
| `CLOUDINARY_API_SECRET`       | Prod     | Cloudinary API secret                            |
| `DATABASE_URL`                | Prod     | Full database URL (overrides individual DB vars) |
| `REDIS_URL`                   | Prod     | Redis connection URL                             |
| `ALLOWED_HOSTS`               | Prod     | Comma-separated allowed hosts                    |
| `CORS_ALLOWED_ORIGINS`        | Prod     | Comma-separated allowed CORS origins             |
| `CSRF_TRUSTED_ORIGINS`        | Prod     | Comma-separated trusted origins for CSRF         |
| `PASSWORD_RESET_FRONTEND_URL` |          | Frontend base URL used in password reset emails  |
| `EMAIL_HOST_USER`             | Prod     | SMTP username (Gmail)                            |
| `EMAIL_HOST_PASSWORD`         | Prod     | SMTP password (Gmail)                            |

---

## Deployment

The project ships with a `render.yaml` for one-click deployment to [Render](https://render.com).

```bash
# Production uses the production settings module
DJANGO_SETTINGS_MODULE=music_app.settings.production
```

The production settings module enables:

- `DEBUG=False` with strict `ALLOWED_HOSTS` and CORS policy
- PostgreSQL via `DATABASE_URL` with SSL
- Cloudinary for media storage (smart routing: images → `image` type, audio → `raw` type)
- Redis channel layer for WebSocket
- Gmail SMTP for transactional email
- Whitenoise for static file serving

---

## Admin Panel

Django admin is available at `/admin/` and provides full CRUD for all entities, including:

- **Tracks** — automatic duration extraction from the uploaded audio file via mutagen
- **Artists** — band membership management, genre assignment, manager linking
- **Albums** — ordered track lists via inline `AlbumTrack`
- **Playlists** — ordered tracks via inline `PlaylistTrack`
- **Lyrics** — static plain text or synced (karaoke-style) line-by-line entries
- **Feed** — posts, comments, likes, reports
- **Chat** — message history per conversation
- **Users** — profile management, follower graph, verification status
- **Notifications** — full notification log per user
- **Legal** — Terms of Service and Privacy Policy document management per language