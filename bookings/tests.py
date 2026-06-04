from datetime import date, time, timedelta

from django.contrib.auth.models import User
from django.core import mail
from django.test import Client, TestCase
from django.urls import reverse

from .models import Booking, Category, Event
from .utils import generate_confirmation_code


class EventBookingTests(TestCase):
    def setUp(self):
        self.client = Client()
        self.category = Category.objects.create(
            name='Music',
            description='Live music events',
        )
        self.event = Event.objects.create(
            title='Summer Concert',
            description='An outdoor concert.',
            category=self.category,
            event_date=date.today() + timedelta(days=30),
            event_time=time(19, 0),
            location='City Arena',
            capacity=100,
        )
        self.user = User.objects.create_user(
            username='alice',
            email='alice@example.com',
            password='SecurePass123!',
        )
        self.staff = User.objects.create_user(
            username='admin',
            email='admin@example.com',
            password='AdminPass123!',
            is_staff=True,
        )

    def test_home_page_lists_events(self):
        response = self.client.get(reverse('home'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Summer Concert')

    def test_search_by_category(self):
        url = reverse('home') + f'?category={self.category.pk}'
        response = self.client.get(url)
        self.assertContains(response, 'Summer Concert')

    def test_search_by_date(self):
        url = reverse('home') + f'?event_date={self.event.event_date.isoformat()}'
        response = self.client.get(url)
        self.assertContains(response, 'Summer Concert')

    def test_event_detail_shows_capacity(self):
        response = self.client.get(reverse('event_detail', args=[self.event.slug]))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, '100')

    def test_user_registration_and_login(self):
        response = self.client.post(reverse('register'), {
            'username': 'bob',
            'email': 'bob@example.com',
            'password1': 'NewUserPass123!',
            'password2': 'NewUserPass123!',
        })
        self.assertEqual(response.status_code, 302)
        self.assertTrue(User.objects.filter(username='bob').exists())

        login_ok = self.client.login(username='bob', password='NewUserPass123!')
        self.assertTrue(login_ok)

    def test_booking_requires_login(self):
        response = self.client.get(reverse('book_event', args=[self.event.slug]))
        self.assertEqual(response.status_code, 302)

    def test_successful_booking_sends_email(self):
        self.client.login(username='alice', password='SecurePass123!')
        response = self.client.post(reverse('book_event', args=[self.event.slug]), {
            'ticket_count': 2,
        })
        self.assertEqual(response.status_code, 302)
        booking = Booking.objects.get(user=self.user, event=self.event)
        self.assertEqual(booking.ticket_count, 2)
        self.assertEqual(booking.status, Booking.Status.CONFIRMED)
        self.assertEqual(len(mail.outbox), 1)
        self.assertIn(booking.confirmation_code, mail.outbox[0].body)

    def test_event_becomes_full(self):
        self.client.login(username='alice', password='SecurePass123!')
        self.client.post(reverse('book_event', args=[self.event.slug]), {
            'ticket_count': 100,
        })
        self.event.refresh_from_db()
        self.assertTrue(self.event.is_full)
        response = self.client.get(reverse('event_detail', args=[self.event.slug]))
        self.assertContains(response, 'Fully booked')

    def test_duplicate_booking_blocked(self):
        self.client.login(username='alice', password='SecurePass123!')
        self.client.post(reverse('book_event', args=[self.event.slug]), {
            'ticket_count': 1,
        })
        response = self.client.post(reverse('book_event', args=[self.event.slug]), {
            'ticket_count': 1,
        })
        self.assertEqual(Booking.objects.filter(user=self.user, event=self.event).count(), 1)

    def test_cancel_booking_frees_seats(self):
        self.client.login(username='alice', password='SecurePass123!')
        self.client.post(reverse('book_event', args=[self.event.slug]), {'ticket_count': 5})
        booking = Booking.objects.get(user=self.user, event=self.event)
        response = self.client.post(reverse('cancel_booking', args=[booking.pk]))
        self.assertEqual(response.status_code, 302)
        booking.refresh_from_db()
        self.assertEqual(booking.status, Booking.Status.CANCELLED)
        self.assertEqual(self.event.seats_remaining, 100)

    def test_staff_can_create_event(self):
        self.client.login(username='admin', password='AdminPass123!')
        response = self.client.post(reverse('event_create'), {
            'title': 'Tech Meetup',
            'description': 'Developers meet.',
            'category': self.category.pk,
            'event_date': (date.today() + timedelta(days=10)).isoformat(),
            'event_time': '14:00',
            'location': 'Innovation Hub',
            'capacity': 50,
            'is_published': True,
        })
        self.assertEqual(response.status_code, 302)
        self.assertTrue(Event.objects.filter(title='Tech Meetup').exists())

    def test_non_staff_cannot_access_manage(self):
        self.client.login(username='alice', password='SecurePass123!')
        response = self.client.get(reverse('manage_dashboard'))
        self.assertEqual(response.status_code, 302)

    def test_confirmation_code_unique(self):
        codes = {generate_confirmation_code() for _ in range(50)}
        self.assertEqual(len(codes), 50)
