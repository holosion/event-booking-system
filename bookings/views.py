from django.contrib import messages
from django.contrib.auth import login
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib.auth.mixins import UserPassesTestMixin
from django.contrib.auth.views import LoginView, LogoutView
from django.db.models import Q
from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse_lazy
from django.views.generic import CreateView, DeleteView, ListView, UpdateView

from .forms import (
    BookingForm,
    CategoryForm,
    EventForm,
    EventSearchForm,
    UserRegisterForm,
)
from .models import Booking, Category, Event
from .utils import generate_confirmation_code, send_booking_confirmation_email


def staff_required(user):
    return user.is_authenticated and (user.is_staff or user.is_superuser)


def home(request):
    events = Event.objects.filter(is_published=True).select_related('category')
    form = EventSearchForm(request.GET or None)
    if form.is_valid():
        q = form.cleaned_data.get('q')
        category = form.cleaned_data.get('category')
        event_date = form.cleaned_data.get('event_date')
        if q:
            events = events.filter(
                Q(title__icontains=q)
                | Q(description__icontains=q)
                | Q(location__icontains=q)
            )
        if category:
            events = events.filter(category=category)
        if event_date:
            events = events.filter(event_date=event_date)
    context = {
        'events': events,
        'search_form': form,
        'featured_count': events.count(),
    }
    return render(request, 'bookings/home.html', context)


def event_detail(request, slug):
    event = get_object_or_404(Event, slug=slug, is_published=True)
    booking_form = None
    user_booking = None
    if request.user.is_authenticated:
        user_booking = Booking.objects.filter(
            user=request.user,
            event=event,
            status=Booking.Status.CONFIRMED,
        ).first()
        if not user_booking and not event.is_full:
            booking_form = BookingForm(event=event)
    context = {
        'event': event,
        'booking_form': booking_form,
        'user_booking': user_booking,
    }
    return render(request, 'bookings/event_detail.html', context)


@login_required
def book_event(request, slug):
    event = get_object_or_404(Event, slug=slug, is_published=True)
    if event.is_full:
        messages.error(request, 'Sorry, this event is fully booked.')
        return redirect('event_detail', slug=slug)

    existing = Booking.objects.filter(
        user=request.user,
        event=event,
        status=Booking.Status.CONFIRMED,
    ).first()
    if existing:
        messages.info(request, 'You already have a booking for this event.')
        return redirect('event_detail', slug=slug)

    if request.method == 'POST':
        form = BookingForm(request.POST, event=event)
        if form.is_valid():
            booking = form.save(commit=False)
            booking.user = request.user
            booking.event = event
            booking.confirmation_code = generate_confirmation_code()
            booking.save()
            try:
                send_booking_confirmation_email(booking)
                messages.success(
                    request,
                    'Booking confirmed! A confirmation email has been sent.',
                )
            except Exception:
                messages.success(
                    request,
                    f'Booking confirmed! Your code: {booking.confirmation_code}',
                )
            return redirect('my_bookings')
    else:
        form = BookingForm(event=event)
    return render(request, 'bookings/book_event.html', {'event': event, 'form': form})


@login_required
def my_bookings(request):
    bookings = Booking.objects.filter(
        user=request.user,
        status=Booking.Status.CONFIRMED,
    ).select_related('event', 'event__category')
    return render(request, 'bookings/my_bookings.html', {'bookings': bookings})


@login_required
def cancel_booking(request, pk):
    booking = get_object_or_404(
        Booking,
        pk=pk,
        user=request.user,
        status=Booking.Status.CONFIRMED,
    )
    if request.method == 'POST':
        booking.status = Booking.Status.CANCELLED
        booking.save()
        messages.success(request, 'Your booking has been cancelled.')
        return redirect('my_bookings')
    return render(request, 'bookings/cancel_booking.html', {'booking': booking})


class RegisterView(CreateView):
    form_class = UserRegisterForm
    template_name = 'bookings/register.html'
    success_url = reverse_lazy('home')

    def form_valid(self, form):
        response = super().form_valid(form)
        login(self.request, self.object)
        messages.success(self.request, 'Welcome! Your account has been created.')
        return response


class CustomLoginView(LoginView):
    template_name = 'bookings/login.html'
    redirect_authenticated_user = True


class CustomLogoutView(LogoutView):
    next_page = 'home'


@user_passes_test(staff_required)
def manage_dashboard(request):
    events = Event.objects.select_related('category').all()[:10]
    categories = Category.objects.all()
    booking_count = Booking.objects.filter(status=Booking.Status.CONFIRMED).count()
    return render(request, 'bookings/manage/dashboard.html', {
        'events': events,
        'categories': categories,
        'booking_count': booking_count,
    })


class StaffRequiredMixin(UserPassesTestMixin):
    def test_func(self):
        return staff_required(self.request.user)


class EventCreateView(StaffRequiredMixin, CreateView):
    model = Event
    form_class = EventForm
    template_name = 'bookings/manage/event_form.html'
    success_url = reverse_lazy('manage_events')

    def form_valid(self, form):
        form.instance.created_by = self.request.user
        messages.success(self.request, 'Event created successfully.')
        return super().form_valid(form)


class EventUpdateView(StaffRequiredMixin, UpdateView):
    model = Event
    form_class = EventForm
    template_name = 'bookings/manage/event_form.html'
    success_url = reverse_lazy('manage_events')
    slug_field = 'slug'
    slug_url_kwarg = 'slug'

    def form_valid(self, form):
        messages.success(self.request, 'Event updated successfully.')
        return super().form_valid(form)


class EventDeleteView(StaffRequiredMixin, DeleteView):
    model = Event
    template_name = 'bookings/manage/event_confirm_delete.html'
    success_url = reverse_lazy('manage_events')
    slug_field = 'slug'
    slug_url_kwarg = 'slug'


class ManageEventListView(StaffRequiredMixin, ListView):
    model = Event
    template_name = 'bookings/manage/event_list.html'
    context_object_name = 'events'
    paginate_by = 12


@user_passes_test(staff_required)
def category_list(request):
    categories = Category.objects.all()
    return render(request, 'bookings/manage/category_list.html', {'categories': categories})


@user_passes_test(staff_required)
def category_create(request):
    if request.method == 'POST':
        form = CategoryForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Category created.')
            return redirect('manage_categories')
    else:
        form = CategoryForm()
    return render(request, 'bookings/manage/category_form.html', {'form': form, 'title': 'Add Category'})


@user_passes_test(staff_required)
def category_update(request, pk):
    category = get_object_or_404(Category, pk=pk)
    if request.method == 'POST':
        form = CategoryForm(request.POST, instance=category)
        if form.is_valid():
            form.save()
            messages.success(request, 'Category updated.')
            return redirect('manage_categories')
    else:
        form = CategoryForm(instance=category)
    return render(
        request,
        'bookings/manage/category_form.html',
        {'form': form, 'title': 'Edit Category'},
    )


@user_passes_test(staff_required)
def category_delete(request, pk):
    category = get_object_or_404(Category, pk=pk)
    if request.method == 'POST':
        category.delete()
        messages.success(request, 'Category deleted.')
        return redirect('manage_categories')
    return render(
        request,
        'bookings/manage/category_confirm_delete.html',
        {'category': category},
    )
