"""
Generate the project documentation PDF (SYSTEM_REPORT.pdf).
Run: python scripts/generate_report.py
"""
from pathlib import Path

from fpdf import FPDF

ROOT = Path(__file__).resolve().parent.parent
OUTPUT = ROOT / 'docs' / 'SYSTEM_REPORT.pdf'


class ReportPDF(FPDF):
    def header(self):
        self.set_font('Helvetica', 'B', 10)
        self.set_text_color(100, 100, 100)
        self.cell(0, 8, 'Event Booking System - Project Report', align='C', new_x='LMARGIN', new_y='NEXT')
        self.ln(2)

    def footer(self):
        self.set_y(-15)
        self.set_font('Helvetica', 'I', 8)
        self.set_text_color(120, 120, 120)
        self.cell(0, 10, f'Page {self.page_no()}', align='C')

    def chapter_title(self, title):
        self.set_font('Helvetica', 'B', 14)
        self.set_text_color(40, 40, 80)
        self.cell(0, 10, title, new_x='LMARGIN', new_y='NEXT')
        self.ln(2)

    def body_text(self, text):
        self.set_font('Helvetica', '', 11)
        self.set_text_color(30, 30, 30)
        self.multi_cell(0, 6, text)
        self.ln(2)


def build_report():
    OUTPUT.parent.mkdir(parents=True, exist_ok=True)
    pdf = ReportPDF()
    pdf.set_auto_page_break(auto=True, margin=20)
    pdf.add_page()

    pdf.set_font('Helvetica', 'B', 22)
    pdf.set_text_color(50, 50, 100)
    pdf.cell(0, 12, 'Event Booking Web Application', new_x='LMARGIN', new_y='NEXT')
    pdf.set_font('Helvetica', '', 12)
    pdf.cell(0, 8, 'Django | SQLite/PostgreSQL | Django Templates', new_x='LMARGIN', new_y='NEXT')
    pdf.ln(8)

    sections = [
        ('1. Introduction', (
            'The Event Booking System is a full-stack web application developed using the Django '
            'framework with Django templates for the presentation layer. The system enables '
            'registered users to browse published events, search by category or date, view seat '
            'availability, and book tickets online. Staff users manage events and categories '
            'through a dedicated management interface. The project demonstrates CRUD operations, '
            'authentication, form validation, email notifications, and deployment readiness.'
        )),
        ('2. Problem Statement', (
            'Manual event ticketing is slow, error-prone, and difficult to scale. Organizers '
            'struggle to track capacity, while attendees lack a single place to discover events '
            'and receive booking confirmations. There is a need for an accessible, web-based '
            'platform that centralizes event listings, enforces capacity limits, and automates '
            'confirmations.'
        )),
        ('3. Objectives', (
            '- Allow users to register, log in, and manage their profile via Django auth.\n'
            '- Display events with date, time, location, category, and capacity.\n'
            '- Indicate when events are sold out based on confirmed bookings.\n'
            '- Enable search/filter by keyword, category, and date.\n'
            '- Process ticket bookings with validation and confirmation emails.\n'
            '- Provide staff CRUD for events and categories.\n'
            '- Deliver a responsive, attractive user interface.\n'
            '- Deploy to Render with automated migrations and static files.'
        )),
        ('4. Methodology', (
            'An iterative software development approach was used: requirements analysis, database '
            'design, implementation of Django models/forms/views/URLs, template and CSS design, '
            'unit testing with Django TestCase, and deployment configuration. Version control '
            'is maintained on GitHub. SQLite is used locally; PostgreSQL on Render via '
            'DATABASE_URL for production persistence.'
        )),
        ('5. System Requirements', (
            'Functional: user registration/login; browse and search events; view event details; '
            'book tickets (authenticated); email confirmation; view/cancel bookings; staff event '
            'and category CRUD.\n\n'
            'Non-functional: responsive UI; form validation; secure password rules; HTTPS on '
            'production; static file serving via WhiteNoise.\n\n'
            'Technical: Python 3.12+, Django 5.x, Gunicorn, SQLite (dev), PostgreSQL (Render).'
        )),
        ('6. System Actors', (
            'Guest: browses events, must register to book.\n'
            'Registered User: books tickets, views/cancels own bookings.\n'
            'Staff/Organizer: creates, updates, deletes events and categories.\n'
            'Administrator: Django admin for full data management.'
        )),
        ('7. System Design - Database Models', (
            'User (Django auth): username, email, password.\n'
            'Category: name, slug, description.\n'
            'Event: title, slug, description, category (FK), event_date, event_time, location, '
            'capacity, image, is_published, created_by (FK User).\n'
            'Booking: user (FK), event (FK), ticket_count, confirmation_code, status, booked_at.\n\n'
            'Derived logic: tickets_sold = sum of confirmed booking ticket_count; '
            'seats_remaining = capacity - tickets_sold; is_full when seats_remaining <= 0.'
        )),
    ]

    for title, body in sections:
        pdf.chapter_title(title)
        pdf.body_text(body)

    pdf.add_page()
    pdf.chapter_title('8. Entity Relationship Diagram')
    pdf.set_font('Courier', '', 9)
    erd = """
    +-------------+       +-------------+       +-------------+
    |    User     |       |  Category   |       |    Event    |
    +-------------+       +-------------+       +-------------+
    | id (PK)     |       | id (PK)     |       | id (PK)     |
    | username    |       | name        |       | title       |
    | email       |       | slug        |       | category_id |
    +------+------+       +------+------+       | created_by  |
           |                     |              | capacity    |
           |                     | 1      N     +------+------+
           |                     +--------------|      |
           | 1                                    N    |
           |         +-------------+                  |
           +---------|   Booking   |------------------+
                     +-------------+
                     | id (PK)     |
                     | user_id(FK) |
                     | event_id(FK)|
                     | ticket_count|
                     | status      |
                     +-------------+
    """
    pdf.multi_cell(0, 5, erd)

    pdf.ln(4)
    pdf.chapter_title('9. Screenshots')
    pdf.body_text(
        'Screenshots should be captured from the running application showing: home page with '
        'event grid and search; event detail with availability; registration/login; booking '
        'confirmation; my bookings list; staff manage dashboard; and event create form. '
        'After deployment, include the live Render URL in the report appendix.'
    )

    pdf.chapter_title('10. Testing Results')
    pdf.body_text(
        'Automated tests (python manage.py test) cover:\n'
        '- Home page and event listing\n'
        '- Search by category and date\n'
        '- User registration and login\n'
        '- Booking requires authentication\n'
        '- Successful booking and confirmation email\n'
        '- Sold-out detection when capacity reached\n'
        '- Duplicate booking prevention\n'
        '- Booking cancellation restores seats\n'
        '- Staff event creation and manage access control\n'
        '- Unique confirmation code generation\n\n'
        'All tests are expected to pass before deployment.'
    )

    pdf.chapter_title('11. Challenges Faced')
    pdf.body_text(
            '- Enforcing capacity across concurrent bookings using aggregated ticket counts.\n'
            '- Conditional unique constraint for one active booking per user per event.\n'
            '- Render ephemeral filesystem: PostgreSQL used in production while SQLite locally.\n'
            '- Email delivery in production requires SMTP environment variables.\n'
            '- Static file serving configured with WhiteNoise and collectstatic.'
    )

    pdf.chapter_title('12. Conclusion')
    pdf.body_text(
        'The Event Booking System successfully meets the project requirements: Django MVC '
        'architecture, SQLite/PostgreSQL storage, template-based frontend, CRUD for staff, '
        'user authentication, search, capacity tracking, and email confirmations. The '
        'interface uses modern typography and responsive layout to attract users.'
    )

    pdf.chapter_title('13. Recommendations')
    pdf.body_text(
            '- Add payment gateway integration for paid events.\n'
            '- Implement QR codes on confirmation emails.\n'
            '- Add waitlist when events are full.\n'
            '- Use Celery for async email and reminders.\n'
            '- Add API layer (Django REST Framework) for mobile apps.\n'
            '- Enable social authentication (Google/GitHub OAuth).'
    )

    pdf.output(OUTPUT)
    print(f'Report saved to {OUTPUT}')


if __name__ == '__main__':
    build_report()
