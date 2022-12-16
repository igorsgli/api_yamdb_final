from django.contrib import admin

from .models import CustomUser


@admin.register(CustomUser)
class CustomUserAdmin(admin.ModelAdmin):
    list_display = ('username', 'email', 'confirmation_code', 'role', 'bio', 'is_staff', 'is_superuser')
    list_editable = ('role', 'is_superuser')
    search_fields = ('username',)
    list_filter = ('role',)
