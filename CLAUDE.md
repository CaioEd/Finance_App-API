# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Common Commands

All workflows are wrapped in the `Makefile` (run `make help` for the menu):

- `make database` — start the PostgreSQL container via `docker-compose.yml` (image: postgres:15, port 5432).
- `make migrations` — `python manage.py makemigrations`.
- `make migrate` — `python manage.py migrate` (requires `.env` to be populated first; see `.env.example`).
- `make run` — `python manage.py runserver` (Django dev server on :8000).
- `make install` / `make freeze` — install or regenerate `requirements.txt`.
- `python manage.py createsuperuser` — create an admin user for `/admin/`.
- `python manage.py test apps.<app>` — run tests for a single app (e.g. `apps.expenses`); each app has its own `tests.py`.

Local Postgres credentials hardcoded in `docker-compose.yml` (db `finance-app-db`, user `finance-user`, password `fadbp01`) must match the `DB_*` values in `.env` for `make migrate`/`make run` to connect.

## Architecture

Single Django 5.1 project (`finance_hub/`) with one Django app package (`apps/`) that contains four logical sub-modules: `users`, `incomes`, `expenses`, `balance`. Only `apps` is registered in `INSTALLED_APPS` — the sub-modules are not separate Django apps, they share `apps/migrations/` and `apps/apps.py`. When adding models in a sub-module, the migration lands under `apps/migrations/`.

### URL surface
All routes are declared in `finance_hub/urls.py`. The router pattern is: each sub-module exposes a DRF `DefaultRouter` from its own `urls.py` (`users`, `incomes`, `expenses`) and is `include()`d under `api/`. `balance` has no router — its `APIView` classes are wired directly in the project `urls.py`. Aggregate endpoints (`/api/incomes/month`, `/api/expenses/month`, `/api/balance/month/`, `/api/balance/date/`, `/api/download/balance/date/`) also live in the project `urls.py` rather than in sub-module routers.

### Auth
JWT via `djangorestframework-simplejwt` is the default DRF authentication class (set globally in `settings.REST_FRAMEWORK`). Login accepts **email + password**, not username — `apps.users.authentication.EmailAuthBackend` is registered first in `AUTHENTICATION_BACKENDS` and looks users up by email. `CustomTokenObtainPairSerializer` (in `apps/users/serializer.py`) injects `username`, `email`, `first_name` into the JWT payload. Logout blacklists the refresh token, so token blacklisting must remain enabled if you change SimpleJWT config.

### Data model
The user model is Django's built-in `auth.User`. `Incomes`, `Expenses`, and `Balance` all have a `ForeignKey(User, related_name='...')`. List/CRUD viewsets scope querysets to `request.user` in `get_queryset` and assign `user=self.request.user` in `perform_create` — preserve this pattern when adding new user-owned resources.

`Balance` is a **derived/cache** model: `BalanceView.get` recomputes monthly totals from `Incomes`/`Expenses` and upserts a `Balance` row per (user, month). Note the field-name mismatch — `Balance.__str__` and `BalanceView` reference `self.data` / `data__year` while the model field is actually `date`; this is a latent bug to be aware of when touching the balance flow.

### PDF generation
`DownloadPdfByDateView` (apps/balance/views.py) uses `reportlab` to render a financial summary PDF in-memory and returns it via `FileResponse`. The logo is loaded from `static/images/finance-logo.png` resolved against `settings.BASE_DIR` — that static directory must exist for the endpoint to work.

### CORS
`CORS_ALLOW_ALL_ORIGINS = True` is hardcoded in settings. This is dev-only — tighten before any non-local deployment.

## Configuration

`.env` is loaded via `python-dotenv` at the top of `finance_hub/settings.py`. Required variables: `SECRET_KEY`, `DB_NAME`, `DB_USER`, `DB_PASSWORD`, `DB_HOST`, `DB_PORT` (see `.env.example`). `DEBUG=True` is hardcoded and `ALLOWED_HOSTS=[]` — both need to be lifted to env vars before production.
