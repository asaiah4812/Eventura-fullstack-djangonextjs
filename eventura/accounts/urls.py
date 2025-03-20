from django.urls import path
from . import views

urlpatterns = [
    path('register/', views.register_user, name='register'),
    path('dashboard/', views.user_dashboard, name='dashboard'),
    path('profile/<str:wallet_address>/', views.user_profile, name='user-profile'),
    path('profile/update/', views.update_profile, name='update-profile'),
    path('verify-token/', views.verify_token, name='verify-token'),
    path('dashboard-stats/', views.get_dashboard_stats, name='dashboard-stats'),
]
