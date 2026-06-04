# Deployment Guide (Render)

## Prerequisites

- GitHub repository: https://github.com/holosion/event-booking-system.git
- [Render](https://render.com) account

## Option A: Blueprint (recommended)

1. Push all project files to your GitHub repo.
2. In Render: **New +** → **Blueprint** → connect `holosion/event-booking-system`.
3. Render reads `render.yaml` and creates the web service + PostgreSQL database.
4. Wait for the first deploy to finish (build runs `build.sh`: install, collectstatic, migrate, seed demo data).
5. The seeded catalog includes 14 categories, 70 events, and static cover artwork from `static/img/events/`.

## Option B: Manual web service

| Setting | Value |
|---------|--------|
| Runtime | Python 3 |
| Build Command | `./build.sh` |
| Start Command | `gunicorn eventbooking.wsgi:application` |

Add environment variables:

| Variable | Value |
|----------|--------|
| `DEBUG` | `False` |
| `DJANGO_SECRET_KEY` | (generate secure random string) |
| `DATABASE_URL` | (from Render PostgreSQL instance) |
| `PYTHON_VERSION` | `3.12.3` |

## After deployment

1. Copy your live URL (e.g. `https://event-booking-system-xxxx.onrender.com`).
2. Add it to your project report and submission.
3. Log in with demo staff: `staff` / `StaffDemo123!` (created by `seed_demo_data` on build).

## Email on production

Set SMTP variables in Render:

- `EMAIL_BACKEND=django.core.mail.backends.smtp.EmailBackend`
- `EMAIL_HOST`, `EMAIL_PORT`, `EMAIL_HOST_USER`, `EMAIL_HOST_PASSWORD`
- `DEFAULT_FROM_EMAIL`

Without these, bookings still work; confirmation codes appear in the success message.

## Demo event images

The seeded event images are stored as static files instead of uploaded media. This keeps the demo catalog reliable on Render's ephemeral filesystem and lets WhiteNoise serve the covers after `collectstatic`.

## Local vs production database

- **Local:** SQLite (`db.sqlite3`)
- **Render:** PostgreSQL via `DATABASE_URL` (persistent, recommended)
