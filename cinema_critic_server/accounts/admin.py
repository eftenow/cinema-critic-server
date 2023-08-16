from django.contrib import admin
from django.contrib.auth import get_user_model
from .models import Profile
from django import forms
from django.contrib.auth.models import Group

UserModel = get_user_model()


class UserChangeForm(forms.ModelForm):
    groups = forms.ModelMultipleChoiceField(
        queryset=Group.objects.all(),
        widget=forms.CheckboxSelectMultiple,
        required=False
    )

    class Meta:
        model = UserModel
        fields = '__all__'


class AppUserAdmin(admin.ModelAdmin):
    list_display = ('username', 'email', 'date_joined', 'is_staff')
    search_fields = ('username', 'email')
    list_filter = ('is_staff', 'date_joined')
    ordering = ('-date_joined',)
    form = UserChangeForm
    administrator_promote_demote_actions = ['promote_regular_to_moderator', 'promote_moderator_to_admin',
                                            'demote_admin_to_moderator',
                                            'demote_moderator_to_regular']

    def promote_regular_to_moderator(self, request, queryset):
        moderator_group, created = Group.objects.get_or_create(name='Moderator')
        for user in queryset:
            if user.groups.filter(name='Regular User').exists():
                user.groups.remove(Group.objects.get(name='Regular User'))
                user.groups.add(moderator_group)

    promote_regular_to_moderator.short_description = "Promote selected Regular Users to Moderator"

    def promote_moderator_to_admin(self, request, queryset):
        admin_group, created = Group.objects.get_or_create(name='Administrator')
        for user in queryset:
            if user.groups.filter(name='Moderator').exists():
                user.groups.remove(Group.objects.get(name='Moderator'))
                user.groups.add(admin_group)

    promote_moderator_to_admin.short_description = "Promote selected Moderators to Administrator"

    def demote_admin_to_moderator(self, request, queryset):
        moderator_group, created = Group.objects.get_or_create(name='Moderator')
        for user in queryset:
            if user.groups.filter(name='Administrator').exists():
                user.groups.remove(Group.objects.get(name='Administrator'))
                user.groups.add(moderator_group)

    demote_admin_to_moderator.short_description = "Demote selected Administrators to Moderator"

    def demote_moderator_to_regular(self, request, queryset):
        regular_group, created = Group.objects.get_or_create(name='Regular User')
        for user in queryset:
            if user.groups.filter(name='Moderator').exists():
                user.groups.remove(Group.objects.get(name='Moderator'))
                user.groups.add(regular_group)

    demote_moderator_to_regular.short_description = "Demote selected Moderators to Regular User"


admin.site.register(UserModel, AppUserAdmin)


class ProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'first_name', 'last_name', 'city', 'country')
    search_fields = ('user__username', 'first_name', 'last_name', 'city', 'country')
    list_filter = ('gender', 'city', 'country')


admin.site.register(Profile, ProfileAdmin)
