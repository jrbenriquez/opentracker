from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as AuthUserAdmin
from tracker.models import Event, User, Team, Status, Type, SubType, Ticket, Activity
from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from django import forms

# Register your models here.

class TrackerUserCreationForm(UserCreationForm):
    error_message = UserCreationForm.error_messages.update({
        'duplicate_username': 'This username has already been taken.'
    })

    class Meta(UserCreationForm.Meta):
        model = User

    def clean_username(self):
        username = self.cleaned_data["username"]
        try:
            User.objects.get(username=username)
        except User.DoesNotExist:
            return username
        raise forms.ValidationError(self.error_messages['duplicate_username'])

class TrackerUserChangeForm(UserChangeForm):
     class Meta(UserChangeForm.Meta):
        model = User

@admin.register(User)
class TrackerUserAdmin(AuthUserAdmin):
    form = TrackerUserChangeForm
    add_form = TrackerUserCreationForm
    fieldsets = AuthUserAdmin.fieldsets + (
            ('User Profile', {'fields': ('team',)}),
    )
    list_display = ('username', 'full_name', 'email', 'team')
    search_fields = ['username'] 
admin.site.register(Event)
admin.site.register(Team)
admin.site.register(Status)
admin.site.register(Type)
admin.site.register(SubType)
admin.site.register(Ticket)
admin.site.register(Activity)
