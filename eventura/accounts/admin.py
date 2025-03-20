from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import User

class CustomUserAdmin(UserAdmin):
    list_display = ('wallet_address', 'is_admin', 'is_active', 'username', 'bio', 'email', 'avatar_url', 'twitter_handle', 'website')
    search_fields = ('wallet_address', 'username', 'email')
    ordering = ('wallet_address',)
    
    # Display all fields in the admin dashboard
    fieldsets = (
        (None, {'fields': ('wallet_address', 'email', 'username', 'bio', 'avatar_url', 'twitter_handle', 'website')}),
        ('Permissions', {'fields': ('is_active', 'is_admin')}),
    )
    
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('wallet_address', 'email', 'username', 'bio', 'avatar_url', 'twitter_handle', 'website', 'is_admin', 'is_active')}
        ),
    )

    filter_horizontal = ()
    list_filter = ('is_active', 'is_admin')

admin.site.register(User, CustomUserAdmin)
