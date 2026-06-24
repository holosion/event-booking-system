# Deployment Guide (Render)

## Why This Setup

Render failed because the account already has one active free-tier PostgreSQL database. Render only allows one active free database per workspace, so this project now deploys without creating a database.

The app uses SQLite for the deadline-safe Render deployment. It will run, seed demo data, and show the full event catalog. For long-term production data, add PostgreSQL later and set `DATABASE_URL`.

## Blueprint Deployment

1. Push all project files to GitHub.
2. In Render, choose **New +** -> **Blueprint**.
3. Connect `holosion/event-booking-system`.
4. Render reads `render.yaml` and creates only the web service.
5. Wait for the deploy to finish.

The start command runs:

```bash
python manage.py migrate --no-input && python manage.py seed_demo_data && gunicorn eventbooking.wsgi:application
```

That creates the SQLite tables and loads 14 categories, 70 events, and cover artwork-backed event listings.

## Manual Web Service Settings

| Setting | Value |
| --- | --- |
| Runtime | Python 3 |
| Build Command | `bash build.sh` |
| Start Command | `python manage.py migrate --no-input && python manage.py seed_demo_data && gunicorn eventbooking.wsgi:application` |

Add environment variables:

| Variable | Value |
| --- | --- |
| `DEBUG` | `False` |
| `DJANGO_SECRET_KEY` | Generate a secure random string |
| `PYTHON_VERSION` | `3.12.3` |
| `ALLOWED_HOSTS` | Your Render hostname |

Do not add `DATABASE_URL` unless you have a PostgreSQL database available.

## After Deployment

1. Copy your live URL, for example `https://event-booking-system-xxxx.onrender.com`.
2. Add it to your project report and submission.
3. Log in with demo staff: `staff` / `StaffDemo123!`.

## Email on Production

Set SMTP variables in Render if you want real email sending:

- `EMAIL_BACKEND=django.core.mail.backends.smtp.EmailBackend`
- `EMAIL_HOST`
- `EMAIL_PORT`
- `EMAIL_HOST_USER`
- `EMAIL_HOST_PASSWORD`
- `DEFAULT_FROM_EMAIL`

Without these, bookings still work; confirmation codes appear in the success message or console.

## Demo Event Images

The seeded event images are stored as static files instead of uploaded media. This keeps the demo catalog reliable on Render and lets WhiteNoise serve the covers after `collectstatic`.
