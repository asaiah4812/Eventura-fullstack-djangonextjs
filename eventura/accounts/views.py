from django.shortcuts import render
from rest_framework import status, viewsets
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework_simplejwt.tokens import RefreshToken
from django.shortcuts import get_object_or_404
from .models import User
from .serializers import UserSerializer, UserDashboardSerializer, UserProfileSerializer
from django.utils import timezone
from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from django.db.models import Sum
from decimal import Decimal

# Create your views here.

@api_view(['POST'])
@permission_classes([AllowAny])
def register_user(request):
    """
    Register a new user with their wallet address
    """
    wallet_address = request.data.get('wallet_address')
    
    if not wallet_address:
        return Response(
            {'error': 'Wallet address is required'}, 
            status=status.HTTP_400_BAD_REQUEST
        )
    
    # Check if user already exists
    if User.objects.filter(wallet_address=wallet_address).exists():
        user = User.objects.get(wallet_address=wallet_address)
        refresh = RefreshToken.for_user(user)
        return Response({
            'user': UserSerializer(user).data,
            'refresh': str(refresh),
            'access': str(refresh.access_token),
        })
    
    # Create new user
    user = User.objects.create_user(wallet_address=wallet_address)
    refresh = RefreshToken.for_user(user)
    
    return Response({
        'user': UserSerializer(user).data,
        'refresh': str(refresh),
        'access': str(refresh.access_token),
    }, status=status.HTTP_201_CREATED)

@api_view(['GET', 'PUT'])
@permission_classes([IsAuthenticated])
def user_profile(request):
    """
    Get or update user profile
    """
    user = request.user
    
    if request.method == 'GET':
        serializer = UserSerializer(user)
        return Response(serializer.data)
    
    elif request.method == 'PUT':
        serializer = UserSerializer(user, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def verify_token(request):
    """
    Verify if the current token is valid
    """
    return Response({'valid': True})

@api_view(['GET', 'PUT'])
@permission_classes([IsAuthenticated])
def user_dashboard(request):
    """
    Get user dashboard information including stats and recent events
    """
    user = request.user
    serializer = UserDashboardSerializer(user)
    return Response(serializer.data)

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def user_profile(request, wallet_address):
    """
    Get public profile information for any user
    """
    user = get_object_or_404(User, wallet_address=wallet_address)
    serializer = UserProfileSerializer(user)
    return Response(serializer.data)

@api_view(['PUT'])
@permission_classes([IsAuthenticated])
def update_profile(request):
    """
    Update the authenticated user's profile
    """
    serializer = UserProfileSerializer(request.user, data=request.data, partial=True)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_dashboard_stats(request):
    """
    Get dashboard statistics for the authenticated user
    """
    try:
        user = request.user
        
        # Get user's events and calculate statistics
        total_events = user.organized_events.count()
        
        # Get upcoming events with proper error handling
        upcoming_events = user.organized_events.filter(
            date__gte=timezone.now()
        ).order_by('date')[:5]
        
        # Calculate total revenue and tickets with default values
        total_revenue = user.organized_events.aggregate(
            total=Sum('revenue')
        )['total'] or Decimal('0.00')
        
        total_tickets = user.organized_events.aggregate(
            total=Sum('tickets_sold')
        )['total'] or 0
        
        # Format the response data
        response_data = {
            'stats': {
                'total_events': total_events,
                'total_revenue': float(total_revenue),
                'total_tickets': total_tickets,
                'avg_event_duration': '2.5h',  # You can calculate this based on your event model
            },
            'upcoming_events': [{
                'id': str(event.id),  # Convert UUID to string if using UUID
                'title': event.title,
                'date': event.date.isoformat() if event.date else None,
                'attendees': event.tickets_sold,
                'progress': int((event.tickets_sold / event.max_capacity * 100) 
                              if event.max_capacity else 0),
            } for event in upcoming_events],
        }
        
        return Response(response_data)
        
    except Exception as e:
        print(f"Dashboard error: {str(e)}")  # For debugging
        return Response(
            {'error': 'Failed to fetch dashboard data', 'detail': str(e)},
            status=status.HTTP_500_INTERNAL_SERVER_ERROR
        )
