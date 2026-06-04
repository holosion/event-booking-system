import secrets
import string

from django.conf import settings
from django.core.mail import send_mail
from django.template.loader import render_to_string


def generate_confirmation_code(length=10):
    alphabet = string.ascii_uppercase + string.digits
    return ''.join(secrets.choice(alphabet) for _ in range(length))


def send_booking_confirmation_email(booking):
    subject = f'Booking confirmed — {booking.event.title}'
    message = render_to_string('bookings/emails/booking_confirmation.txt', {
        'booking': booking,
        'event': booking.event,
        'user': booking.user,
    })
    recipient = booking.user.email
    if not recipient:
        return False
    send_mail(
        subject,
        message,
        settings.DEFAULT_FROM_EMAIL,
        [recipient],
        fail_silently=False,
    )
    return True
