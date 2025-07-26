from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import CustomUser

class CustomUserAdmin(UserAdmin):
    # Fields to display in the list view
    list_display = ('username', 'email', 'date_of_birth', 'is_staff')
    
    # Fields to use in the add form
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('username', 'email', 'date_of_birth', 'profile_picture', 'password1', 'password2'),
        }),
    )

    # Fields to use in the edit form
    fieldsets = (
        (None, {'fields': ('username', 'password')}),
        ('Personal info', {'fields': ('email', 'date_of_birth', 'profile_picture')}),
        ('Permissions', {'fields': ('is_active', 'is_staff', 'is_superuser', 'groups', 'user_permissions')}),
        ('Important dates', {'fields': ('last_login', 'date_joined')}),
    )

# Register the custom user model with the admin site
admin.site.register(CustomUser, CustomUserAdmin)
