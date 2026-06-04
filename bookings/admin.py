from django.contrib import admin

from .models import Booking, Category, Event


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'slug')
    prepopulated_fields = {'slug': ('name',)}


@admin.register(Event)
class EventAdmin(admin.ModelAdmin):
    list_display = (
        'title',
        'category',
        'event_date',
        'event_time',
        'location',
        'capacity',
        'is_published',
    )
    list_filter = ('category', 'event_date', 'is_published')
    search_fields = ('title', 'location', 'description')
    prepopulated_fields = {'slug': ('title',)}


@admin.register(Booking)
class BookingAdmin(admin.ModelAdmin):
    list_display = (
        'confirmation_code',
        'user',
        'event',
        'ticket_count',
        'status',
        'booked_at',
    )
    list_filter = ('status', 'booked_at')
    search_fields = ('confirmation_code', 'user__username', 'event__title')
