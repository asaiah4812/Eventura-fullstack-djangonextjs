from django.contrib import admin
from .models import Event, Ticket
# Register your models here.

@admin.register(Event)
class EventAdmin(admin.ModelAdmin):
    list_display = 'organizer', 'name', 'date', 'location', 'ticket_price', 'total_tickets', 'available_tickets', 'organizer_wallet', 'image_url', 'created_at', 'updated_at'
