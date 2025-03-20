from rest_framework import generics
from rest_framework.permissions import IsAuthenticated
from .models import Event
from .serializers import EventSerializer

class EventListView(generics.ListAPIView):
    queryset = Event.objects.all()
    serializer_class = EventSerializer

class UserEventListView(generics.ListAPIView):
    serializer_class = EventSerializer
    
    def get_queryset(self):
        wallet_address = self.kwargs['wallet_address']
        return Event.objects.filter(creator__wallet_address=wallet_address)
