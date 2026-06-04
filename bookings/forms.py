from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError

from .models import Booking, Category, Event


class UserRegisterForm(UserCreationForm):
    email = forms.EmailField(required=True)

    class Meta:
        model = User
        fields = ('username', 'email', 'password1', 'password2')

    def save(self, commit=True):
        user = super().save(commit=False)
        user.email = self.cleaned_data['email']
        if commit:
            user.save()
        return user


class EventSearchForm(forms.Form):
    q = forms.CharField(
        required=False,
        label='Search',
        widget=forms.TextInput(attrs={
            'placeholder': 'Search events...',
            'class': 'styled-input',
        }),
    )
    category = forms.ModelChoiceField(
        queryset=Category.objects.all(),
        required=False,
        empty_label='All categories',
        widget=forms.Select(attrs={'class': 'styled-input'}),
    )
    event_date = forms.DateField(
        required=False,
        widget=forms.DateInput(attrs={'type': 'date', 'class': 'styled-input'}),
        label='Date',
    )


class BookingForm(forms.ModelForm):
    class Meta:
        model = Booking
        fields = ('ticket_count',)
        widgets = {
            'ticket_count': forms.NumberInput(attrs={'class': 'styled-input'}),
        }

    def __init__(self, *args, event=None, **kwargs):
        self.event = event
        super().__init__(*args, **kwargs)
        if event:
            remaining = event.seats_remaining
            self.fields['ticket_count'].widget.attrs.update({
                'min': 1,
                'max': max(remaining, 1),
                'class': 'styled-input',
            })

    def clean_ticket_count(self):
        count = self.cleaned_data['ticket_count']
        if not self.event:
            return count
        if self.event.is_full:
            raise ValidationError('This event is fully booked.')
        if count > self.event.seats_remaining:
            raise ValidationError(
                f'Only {self.event.seats_remaining} seat(s) remaining.'
            )
        return count


class EventForm(forms.ModelForm):
    class Meta:
        model = Event
        fields = (
            'title',
            'description',
            'category',
            'event_date',
            'event_time',
            'location',
            'capacity',
            'image',
            'is_published',
        )
        widgets = {
            'title': forms.TextInput(attrs={'class': 'styled-input'}),
            'description': forms.Textarea(attrs={'rows': 5, 'class': 'styled-input'}),
            'location': forms.TextInput(attrs={'class': 'styled-input'}),
            'capacity': forms.NumberInput(attrs={'class': 'styled-input'}),
            'event_date': forms.DateInput(attrs={'type': 'date', 'class': 'styled-input'}),
            'event_time': forms.TimeInput(attrs={'type': 'time', 'class': 'styled-input'}),
            'category': forms.Select(attrs={'class': 'styled-input'}),
        }


class CategoryForm(forms.ModelForm):
    class Meta:
        model = Category
        fields = ('name', 'description')
