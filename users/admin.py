from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import Userm

class CustomUserAdmin(UserAdmin):
    model = Userm
    list_display = ['email', 'role', 'is_active', 'is_staff', 'is_superuser']
    list_filter = ['is_staff', 'is_superuser', 'role', 'is_active']
    search_fields = ['email']
    ordering = ['email']
    
    fieldsets = (
        (None, {'fields': ('email', 'password')}),
        ('Personal info', {'fields': ('role',)}),
        ('Permissions', {'fields': ('is_active', 'is_staff', 'is_superuser', 'groups', 'user_permissions')}),
        ('Important dates', {'fields': ('last_login',)}),
    )
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'password1', 'password2', 'role', 'is_active', 'is_staff', 'is_superuser'),
        }),
    )

admin.site.register(Userm, CustomUserAdmin)
