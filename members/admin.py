from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from .forms import CustomUserCreationForm, CustomUserChangeForm
from .models import Member


class CustomUserAdmin(UserAdmin):
    add_form = CustomUserCreationForm
    form = CustomUserChangeForm
    model = Member
    list_display = ('username', 'is_staff', 'is_approved', 'is_activated',)
    list_filter = ('username', 'is_staff', 'is_approved', 'is_activated',)
    fieldsets = (
        ('Personal Information', {'fields': ('first_name', 'last_name', 'username', 'photo')}),
        ('Corporate Settings', {'fields': ('department', 'position', 'company', 'items_per_page')}),
        ('Permissions', {'fields': ('is_staff', 'is_approved', 'is_activated')}),
    )
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('username', 'password1', 'password2', 'is_staff', 'is_activated', 'is_approved' , 'photo')}
        ),
    )
    search_fields = ('username',)
    ordering = ('username',)

    list_display = ('id', 'first_name', 'last_name', 'username','is_activated', 'is_approved',)
    #list_display = ('id', 'email', 'is_developer', 'is_seller')

admin.site.register(Member, CustomUserAdmin)