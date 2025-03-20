from django.urls import path
from . import views

urlpatterns = [
    path('events/', views.EventListView.as_view(), name='event-list'),
    path('events/user/<str:wallet_address>/', views.UserEventListView.as_view(), name='user-events'),
    # Add other event-related URLs
]
