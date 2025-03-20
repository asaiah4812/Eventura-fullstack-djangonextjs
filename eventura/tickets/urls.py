from django.urls import path
from . import views

urlpatterns = [
    path('tickets/user/<str:wallet_address>/', views.UserTicketListView.as_view(), name='user-tickets'),
    # Add other ticket-related URLs
]