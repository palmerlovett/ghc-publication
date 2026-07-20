# Django Project

A Django 6 web project. The root of the repo is the Django project root (`manage.py` lives here).

## Run & Operate

- Django dev server runs via the "Django Dev Server" workflow on port 8000
- `python manage.py runserver 0.0.0.0:8000` — run manually
- `python manage.py migrate` — apply database migrations
- `python manage.py createsuperuser` — create an admin user
- `python manage.py startapp <name>` — add a new Django app

## Stack

- Python 3.13
- Django 6.0.7
- SQLite (default, `db.sqlite3` at project root)

## Where things live

- `manage.py` — Django management entry point (project root)
- `django_project/` — Django config package (settings, urls, wsgi, asgi)
- `db.sqlite3` — SQLite database

## User preferences

- User manages default templates themselves, inside `django_project/` (no separate app for them).
