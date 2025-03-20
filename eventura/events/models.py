from django.db import models
import uuid
from django.conf import settings

class Event(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    organizer = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='organized_events')
    name = models.CharField(max_length=255)
    description = models.TextField()
    date = models.DateTimeField()
    location = models.CharField(max_length=255)
    ticket_price = models.DecimalField(max_digits=10, decimal_places=2)
    total_tickets = models.IntegerField()
    available_tickets = models.IntegerField()
    organizer_wallet = models.CharField(max_length=255)
    image_url = models.URLField(max_length=500, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['date']

    def __str__(self):
        return self.name

    @property
    def tickets_sold(self):
        return self.total_tickets - self.available_tickets

    @property
    def revenue(self):
        return self.tickets_sold * self.ticket_price

class Ticket(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    event = models.ForeignKey(Event, on_delete=models.CASCADE, related_name='tickets')
    owner_wallet = models.CharField(max_length=255)
    purchase_date = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-purchase_date']
        # Ensure a user can't buy multiple tickets for the same event
        unique_together = ['event', 'owner_wallet']

    def __str__(self):
        return f"Ticket for {self.event.name} - {self.owner_wallet}"

    def save(self, *args, **kwargs):
        # Check if this is a new ticket being created
        if not self.pk:
            # Ensure there are available tickets
            if self.event.available_tickets <= 0:
                raise ValueError("No tickets available for this event")
            
            # Decrease available tickets
            self.event.available_tickets -= 1
            self.event.save()
        
        super().save(*args, **kwargs)
