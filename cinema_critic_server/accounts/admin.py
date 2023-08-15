from django.contrib import admin
from django.contrib.auth import get_user_model
from .models import Profile

UserModel = get_user_model()


class AppUserAdmin(admin.ModelAdmin):
    list_display = ('username', 'email', 'date_joined', 'is_staff')
    search_fields = ('username', 'email')
    list_filter = ('is_staff', 'date_joined')
    ordering = ('-date_joined',)


admin.site.register(UserModel, AppUserAdmin)


class ProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'first_name', 'last_name', 'city', 'country')
    search_fields = ('user__username', 'first_name', 'last_name', 'city', 'country')
    list_filter = ('gender', 'city', 'country')


admin.site.register(Profile, ProfileAdmin)
