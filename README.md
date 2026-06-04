# Event Booking System

A full-featured event booking web application built with **Django**, **Django templates**, and **SQLite** (local) / **PostgreSQL** (Render production).

Repository: [https://github.com/holosion/event-booking-system.git](https://github.com/holosion/event-booking-system.git)

## Features

- User registration, login, and logout
- Browse and search events (keyword, category, date)
- Event details with capacity and sold-out status
- Ticket booking with email confirmation
- My bookings and cancellation
- Staff dashboard: CRUD for events and categories
- Seeded catalog with 14 categories, 70 demo events, and static cover artwork
- Responsive dark-theme UI (CSS + light JavaScript)

## Quick Start (Local)

```bash
python -m venv venv
venv\Scripts\activate          # Windows
pip install -r requirements.txt
python manage.py migrate
python manage.py seed_demo_data        # loads 70 events with cover images
python manage.py createsuperuser   # optional
python manage.py runserver
```

Open [http://127.0.0.1:8000/](http://127.0.0.1:8000/)

**Demo staff account** (after `seed_demo_data`): `staff` / `StaffDemo123!`

## Run Tests

```bash
python manage.py test
```

## Deliverables

| Item | Location |
|------|----------|
| PDF report | `docs/SYSTEM_REPORT.pdf` — generate with `python scripts/generate_report.py` |
| Source ZIP | `deliverables/event-booking-system.zip` — `python scripts/create_zip.py` |
| Live URL | Set after Render deploy (see below) |

## Deploy to Render

1. Push this project to GitHub (`holosion/event-booking-system`).
2. In [Render Dashboard](https://dashboard.render.com/), **New → Blueprint** and connect the repo (uses `render.yaml`), or **New Web Service** manually:
   - **Build command:** `./build.sh`
   - **Start command:** `gunicorn eventbooking.wsgi:application`
3. Add a **PostgreSQL** database (free tier) and set `DATABASE_URL` (Blueprint does this automatically).
4. Environment variables:
   - `DJANGO_SECRET_KEY` — generate a secure random string
   - `DEBUG` — `False`
   - `ALLOWED_HOSTS` — your-app.onrender.com
   - Optional email: `EMAIL_BACKEND=django.core.mail.backends.smtp.EmailBackend`, `EMAIL_HOST_USER`, `EMAIL_HOST_PASSWORD`, `DEFAULT_FROM_EMAIL`
5. The build runs migrations and `seed_demo_data`, so the first deploy includes the demo catalog.
6. After deploy, copy the service URL into your report and submission.

## Project Structure

```
eventbooking/     # Django project settings
bookings/         # Main app (models, views, forms, tests)
templates/        # Django HTML templates
static/           # CSS and JavaScript
static/img/events # Demo event cover artwork used by the seed command
docs/             # Report PDF and ERD
scripts/          # Report and ZIP generators
```

## System Actors

- **Guest** — view events
- **User** — book and manage tickets
- **Staff** — manage events/categories at `/manage/`
- **Admin** — Django admin panel

## License

Academic / project use.
