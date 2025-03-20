from rest_framework import generics
from rest_framework.permissions import IsAuthenticated
from .models import Ticket
from .serializers import TicketSerializer

class UserTicketListView(generics.ListAPIView):
    serializer_class = TicketSerializer
    
    def get_queryset(self):
        wallet_address = self.kwargs['wallet_address']
# Create your views here.
