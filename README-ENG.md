# Orrin Backend

[Українська](README.md) | **[English](README-ENG.md)**

Backend part of **Orrin** — a music streaming web application with social network features.

## 📋 Project Description

Orrin is a web application that combines music streaming and social networking. Users can listen to music, manage a personal library of tracks and artists, share thoughts through a social feed, chat in real time, and follow friends' listening activity.

The backend is built on **Django REST Framework** with WebSocket support via **Django Channels** and an asynchronous transport layer powered by **Redis**.

---

## 🏗️ Architecture

The project is split into independent Django applications organized by domain:

| App | Responsibility |
|---|---|
| `orrin` | Tracks, artists, genres, playlists |
| `users` | Authentication, profiles, follows, notifications |
| `library` | Liked tracks, followed artists, listening history |
| `feed` | Posts, comments, reactions (likes, reposts, saves) |
| `chat` | Private messaging between users (WebSocket) |
| `stats` | Personal listening statistics |

---

## ⚙️ Tech Stack

- **Python 3.13** / **Django 5.2**
- **Django REST Framework** — REST API layer
- **Django Channels** + **Daphne** — ASGI server, WebSocket support
- **channels-redis** — channel layer backend for Channels
- **PostgreSQL 16** — primary relational database
- **Redis 7** — message broker for WebSocket and Channels
- **Simple JWT** — JWT authentication (access + refresh tokens)
- **Google OAuth2** — sign in with Google account
- **drf-spectacular** — automatic OpenAPI schema generation (Swagger / ReDoc)
- **mutagen** — audio file metadata parsing (track duration)
- **python-slugify** — automatic slug generation

---

## 🚀 Getting Started

### Prerequisites

- Docker and Docker Compose

### Steps

```bash
# 1. Clone the repository
git clone <repo-url>
cd orrin-backend

# 2. Create .env from the example
cp .env.example .env

# 3. Start containers
docker-compose up --build

# 4. Apply migrations
docker-compose exec web python manage.py migrate

# 5. (Optional) Create a superuser
docker-compose exec web python manage.py createsuperuser
```

Server will be available at: `http://localhost:8000`  
Swagger API docs: `http://localhost:8000/api/v1/docs/schema/swagger-ui/`

---

## 🔑 Authentication

All protected endpoints use **JWT Bearer** tokens.

| Endpoint | Method | Description |
|---|---|---|
| `/api/v1/auth/token/` | POST | Obtain access + refresh token |
| `/api/v1/auth/token/refresh/` | POST | Refresh access token |
| `/api/v1/auth/register/` | POST | Register a new user |
| `/api/v1/auth/google/login/` | POST | Sign in with Google OAuth2 |
| `/api/v1/auth/password/reset/` | POST | Request password reset |
| `/api/v1/auth/password/reset/confirm/` | POST | Confirm password reset |

---

## 📡 API — Endpoint Groups

### Tracks & Artists
- `GET /api/v1/tracks/` — track list with search and ordering
- `GET /api/v1/tracks/{slug}/` — track details
- `GET /api/v1/artists/` — artist list
- `GET /api/v1/artists/{slug}/` — artist profile with popular tracks and similar artists

### Library
- `GET /api/v1/library/` — aggregated overview: liked tracks, followed artists, playlists
- `GET /api/v1/library/liked/` — liked tracks
- `POST /api/v1/tracks/{slug}/like/` — toggle track like
- `GET /api/v1/library/artists/` — followed artists
- `POST /api/v1/artists/{slug}/follow/` — toggle artist follow
- `GET/POST/DELETE /api/v1/history/` — manage listening history

### Playlists
- `GET/POST /api/v1/library/playlists/` — list playlists / create
- `GET/PATCH/DELETE /api/v1/library/playlists/{id}/` — details, edit, delete
- `POST /api/v1/library/playlists/{id}/tracks/` — add track
- `DELETE /api/v1/library/playlists/{id}/tracks/{slug}/` — remove track

### Feed
- `GET /api/v1/feed/` — post feed with filtering (`feed_type`, `sort`, `content_type`) and pagination
- `POST /api/v1/feed/` — create a post
- `GET/PATCH/DELETE /api/v1/feed/posts/{id}/` — details, edit, delete
- `POST /api/v1/feed/posts/{id}/like/` — like
- `POST /api/v1/feed/posts/{id}/repost/` — repost
- `POST /api/v1/feed/posts/{id}/save/` — save
- `GET/POST /api/v1/feed/posts/{id}/comments/` — comments

### Users & Social
- `GET/PATCH /api/v1/users/me/` — own profile
- `GET /api/v1/users/{username}/` — any user's profile
- `POST /api/v1/users/{username}/follow/` — toggle follow
- `GET /api/v1/users/{username}/followers/` — followers list
- `GET /api/v1/users/{username}/following/` — following list
- `GET /api/v1/users/search/?search=` — user search
- `GET /api/v1/friends/activity/` — friends' recent listening activity

### Chat
- `GET/POST /api/v1/chats/` — list chats / create chat
- `GET /api/v1/chats/{id}/` — chat details
- `GET/POST /api/v1/chats/{id}/messages/` — chat messages

### Statistics
- `GET /api/v1/stats/top-tracks/` — top tracks by play count
- `GET /api/v1/stats/top-artists/` — top artists
- `GET /api/v1/stats/top-albums/` — top by album-play statistics

---

## 🔌 WebSocket

Connection requires a JWT token as a query parameter.

| URL | Purpose |
|---|---|
| `ws://host/ws/notifications/?token=<access>` | Push notifications for the current user |
| `ws://host/ws/chat/{chat_id}/?token=<access>` | Real-time chat messages |

**Chat events (client → server):**
- `send_message` — send a message (fields: `text`, `trackId`)
- `typing_start` / `typing_stop` — typing indicator

**Chat events (server → client):**
- `receive_message` — new incoming message
- `typing_start` / `typing_stop` — typing indicator from the other participant

---

## 🗂️ Environment Variables

| Variable | Description |
|---|---|
| `SECRET_KEY` | Django secret key |
| `POSTGRES_DB` | Database name |
| `POSTGRES_USER` | PostgreSQL user |
| `POSTGRES_PASSWORD` | PostgreSQL password |
| `DB_HOST` | Database host |
| `DB_PORT` | Database port (default 5432) |
| `GOOGLE_CLIENT_ID` | Client ID for Google OAuth2 |
| `ALLOWED_HOSTS` | Allowed hosts (production, comma-separated) |
| `CORS_ALLOWED_ORIGINS` | Allowed CORS origins (production, comma-separated) |
| `PASSWORD_RESET_FRONTEND_URL` | Frontend URL used in password reset links |

---

## 🛠️ Admin Panel

Django admin is available at `/admin/`. Supports:

- Track management with automatic duration calculation from the audio file
- Artist management: band membership, genres, managers
- Full CRUD for all project entities