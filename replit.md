# Django Project

A basic Django 6 web project scaffolded with `django-admin startproject`.

## Run & Operate

- Django dev server runs via the "Django Dev Server" workflow on port 8000
- `cd django_project && python manage.py runserver 0.0.0.0:8000` — run manually
- `cd django_project && python manage.py migrate` — apply database migrations
- `cd django_project && python manage.py createsuperuser` — create an admin user
- `cd django_project && python manage.py startapp <name>` — add a new app

## Stack

- pnpm workspaces, Node.js 24, TypeScript 5.9
- API: Express 5
- DB: PostgreSQL + Drizzle ORM
- Validation: Zod (`zod/v4`), `drizzle-zod`
- API codegen: Orval (from OpenAPI spec)
- Build: esbuild (CJS bundle)

## Where things live

_Populate as you build — short repo map plus pointers to the source-of-truth file for DB schema, API contracts, theme files, etc._

## Architecture decisions

_Populate as you build — non-obvious choices a reader couldn't infer from the code (3-5 bullets)._

## Product

_Describe the high-level user-facing capabilities of this app once they exist._

## User preferences

_Populate as you build — explicit user instructions worth remembering across sessions._

## Gotchas

_Populate as you build — sharp edges, "always run X before Y" rules._

## Pointers

- See the `pnpm-workspace` skill for workspace structure, TypeScript setup, and package details
