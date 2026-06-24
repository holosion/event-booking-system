# Event Booking System

A full-featured event booking web application built with **Django**, **Django templates**, and **SQLite**.

Repository: [https://github.com/holosion/event-booking-system.git](https://github.com/holosion/event-booking-system.git)

## Features

- User registration, login, and logout
- Browse and search events by keyword, category, and date
- Event details with capacity and sold-out status
- Ticket booking with email confirmation
- My bookings and cancellation
- Staff dashboard for event and category management
- Seeded catalog with 14 categories, 70 demo events, and static cover artwork
- Responsive dark-theme UI with CSS and light JavaScript

## Quick Start

```bash
python -m venv venv
venv\Scripts\activate
pip install -r requirements.txt
python manage.py migrate
python manage.py seed_demo_data
python manage.py createsuperuser
python manage.py runserver
```

Open [http://127.0.0.1:8000/](http://127.0.0.1:8000/)

Demo staff account after `seed_demo_data`: `staff` / `StaffDemo123!`

## Run Tests

```bash
python manage.py test
```

## Deploy to Render

This repo is set up to deploy on Render without creating a new Render Postgres database, so it avoids the free-tier limit of one active free database per workspace.

1. Push this project to GitHub.
2. In [Render Dashboard](https://dashboard.render.com/), create a **New Blueprint** and connect this repo.
3. Render reads `render.yaml` and creates the web service.
4. The service start command runs migrations and loads the seeded event catalog.

Manual web service settings:

| Setting | Value |
| --- | --- |
| Runtime | Python |
| Build command | `bash build.sh` |
| Start command | `python manage.py migrate --no-input && python manage.py seed_demo_data && gunicorn eventbooking.wsgi:application` |

Environment variables:

| Variable | Value |
| --- | --- |
| `DJANGO_SECRET_KEY` | Generate a secure random string |
| `DEBUG` | `False` |
| `ALLOWED_HOSTS` | Your Render hostname, for example `event-booking-system.onrender.com` |

Note: This deadline-safe free-tier setup uses SQLite. It runs and shows the full demo catalog, but long-term production bookings should use PostgreSQL by adding `DATABASE_URL`.

## Deliverables

| Item | Location |
| --- | --- |
| PDF report | `docs/SYSTEM_REPORT.pdf` - generate with `python scripts/generate_report.py` |
| Source ZIP | `deliverables/event-booking-system.zip` - generate with `python scripts/create_zip.py` |
| Live URL | Set after Render deploy |

## Project Structure

```text
eventbooking/      Django project settings
bookings/          Main app with models, views, forms, and tests
templates/         Django HTML templates
static/            CSS, JavaScript, and static images
static/img/events  Demo event cover artwork used by the seed command
docs/              Report PDF and ERD
scripts/           Report and ZIP generators
```

## System Actors

- Guest: view events
- User: book and manage tickets
- Staff: manage events and categories at `/manage/`
- Admin: Django admin panel

## License

Academic / project use.
