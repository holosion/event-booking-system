from pathlib import PurePosixPath

from django.conf import settings
from django.core.validators import MinValueValidator
from django.db import models
from django.db.models import Sum
from django.templatetags.static import static
from django.utils.text import slugify


class Category(models.Model):
    name = models.CharField(max_length=100, unique=True)
    slug = models.SlugField(max_length=120, unique=True, blank=True)
    description = models.TextField(blank=True)

    class Meta:
        verbose_name_plural = 'categories'
        ordering = ['name']

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.name


class Event(models.Model):
    SEEDED_IMAGE_PREFIX = 'seeded_events/'

    title = models.CharField(max_length=200)
    slug = models.SlugField(max_length=220, unique=True, blank=True)
    description = models.TextField()
    category = models.ForeignKey(
        Category,
        on_delete=models.PROTECT,
        related_name='events',
    )
    event_date = models.DateField()
    event_time = models.TimeField()
    location = models.CharField(max_length=255)
    capacity = models.PositiveIntegerField(validators=[MinValueValidator(1)])
    image = models.ImageField(upload_to='events/', blank=True, null=True)
    is_published = models.BooleanField(default=True)
    created_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='created_events',
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['event_date', 'event_time']

    def save(self, *args, **kwargs):
        if not self.slug:
            base = slugify(self.title)[:200]
            slug = base
            counter = 1
            while Event.objects.filter(slug=slug).exclude(pk=self.pk).exists():
                slug = f'{base}-{counter}'
                counter += 1
            self.slug = slug
        super().save(*args, **kwargs)

    @property
    def tickets_sold(self):
        total = self.bookings.filter(status=Booking.Status.CONFIRMED).aggregate(
            total=Sum('ticket_count')
        )['total']
        return total or 0

    @property
    def seats_remaining(self):
        return max(self.capacity - self.tickets_sold, 0)

    @property
    def is_full(self):
        return self.seats_remaining <= 0

    @property
    def display_image_url(self):
        if not self.image:
            return ''

        image_name = self.image.name
        if image_name.startswith(self.SEEDED_IMAGE_PREFIX):
            filename = PurePosixPath(image_name).name
            return static(f'img/events/{filename}')

        return self.image.url

    def __str__(self):
        return self.title


class Booking(models.Model):
    class Status(models.TextChoices):
        CONFIRMED = 'confirmed', 'Confirmed'
        CANCELLED = 'cancelled', 'Cancelled'

    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='bookings',
    )
    event = models.ForeignKey(
        Event,
        on_delete=models.CASCADE,
        related_name='bookings',
    )
    ticket_count = models.PositiveIntegerField(
        default=1,
        validators=[MinValueValidator(1)],
    )
    confirmation_code = models.CharField(max_length=12, unique=True, editable=False)
    status = models.CharField(
        max_length=20,
        choices=Status.choices,
        default=Status.CONFIRMED,
    )
    booked_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-booked_at']
        constraints = [
            models.UniqueConstraint(
                fields=['user', 'event'],
                condition=models.Q(status='confirmed'),
                name='unique_active_booking_per_user_event',
            ),
        ]

    def __str__(self):
        return f'{self.user.username} — {self.event.title} ({self.confirmation_code})'
