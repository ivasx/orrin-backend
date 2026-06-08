FROM python:3.13-slim

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

RUN python manage.py collectstatic --noinput --settings=music_app.settings.production

EXPOSE 8000

CMD ["daphne", "-b", "0.0.0.0", "-p", "8000", "--verbosity", "1", "music_app.asgi:application"]