from rest_framework import serializers
from .models import User

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'wallet_address', 'email', 'username', 'bio', 
                 'avatar_url', 'twitter_handle', 'website', 'created_at', 
                 'updated_at', 'is_active']
        read_only_fields = ['id', 'wallet_address', 'created_at', 'updated_at', 'is_active']

class UserDashboardSerializer(serializers.ModelSerializer):
    total_events_organized = serializers.IntegerField(read_only=True)
    total_tickets_sold = serializers.IntegerField(read_only=True)
    total_revenue = serializers.DecimalField(max_digits=10, decimal_places=2, read_only=True)

    class Meta:
        model = User
        fields = ['id', 'wallet_address', 'username', 'avatar_url', 
                 'total_events_organized', 'total_tickets_sold', 'total_revenue']
        read_only_fields = ['id', 'wallet_address']

class UserProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['username', 'bio', 'avatar_url', 'twitter_handle', 
                 'website', 'email']
