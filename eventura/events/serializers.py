from rest_framework import serializers
from .models import Event, Ticket

class EventSerializer(serializers.ModelSerializer):
    class Meta:
        model = Event
        fields = [
            'id',
            'name',
            'description',
            'date',
            'location',
            'ticket_price',
            'total_tickets',
            'available_tickets',
            'organizer_wallet',
            'image_url',
            'created_at',
            'updated_at'
        ]
        read_only_fields = ['id', 'created_at', 'updated_at']

    def validate(self, data):
        # Ensure total_tickets is positive
        if data.get('total_tickets', 0) <= 0:
            raise serializers.ValidationError("Total tickets must be greater than 0")
        
        # If this is a new event, set available_tickets equal to total_tickets
        if not self.instance:
            data['available_tickets'] = data['total_tickets']
        
        # Ensure ticket_price is positive
        if data.get('ticket_price', 0) < 0:
            raise serializers.ValidationError("Ticket price cannot be negative")
        
        return data

class TicketSerializer(serializers.ModelSerializer):
    event = EventSerializer(read_only=True)
    event_id = serializers.UUIDField(write_only=True)

    class Meta:
        model = Ticket
        fields = [
            'id',
            'event',
            'event_id',
            'owner_wallet',
            'purchase_date'
        ]
        read_only_fields = ['id', 'purchase_date']

    def create(self, validated_data):
        event_id = validated_data.pop('event_id')
        try:
            event = Event.objects.get(id=event_id)
        except Event.DoesNotExist:
            raise serializers.ValidationError("Event not found")

        if event.available_tickets <= 0:
            raise serializers.ValidationError("No tickets available for this event")

        # Check if user already has a ticket for this event
        if Ticket.objects.filter(
            event=event,
            owner_wallet=validated_data['owner_wallet']
        ).exists():
            raise serializers.ValidationError("You already have a ticket for this event")

        return Ticket.objects.create(event=event, **validated_data)