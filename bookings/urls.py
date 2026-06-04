from django.urls import path

from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('events/<slug:slug>/', views.event_detail, name='event_detail'),
    path('events/<slug:slug>/book/', views.book_event, name='book_event'),
    path('my-bookings/', views.my_bookings, name='my_bookings'),
    path('bookings/<int:pk>/cancel/', views.cancel_booking, name='cancel_booking'),
    path('register/', views.RegisterView.as_view(), name='register'),
    path('login/', views.CustomLoginView.as_view(), name='login'),
    path('logout/', views.CustomLogoutView.as_view(), name='logout'),
    path('manage/', views.manage_dashboard, name='manage_dashboard'),
    path('manage/events/', views.ManageEventListView.as_view(), name='manage_events'),
    path('manage/events/add/', views.EventCreateView.as_view(), name='event_create'),
    path('manage/events/<slug:slug>/edit/', views.EventUpdateView.as_view(), name='event_update'),
    path('manage/events/<slug:slug>/delete/', views.EventDeleteView.as_view(), name='event_delete'),
    path('manage/categories/', views.category_list, name='manage_categories'),
    path('manage/categories/add/', views.category_create, name='category_create'),
    path('manage/categories/<int:pk>/edit/', views.category_update, name='category_update'),
    path('manage/categories/<int:pk>/delete/', views.category_delete, name='category_delete'),
]
