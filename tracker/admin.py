from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as AuthUserAdmin
from tracker.models import Event, User, Team, Status, Type, SubType, Ticket, Activity
from tracker.forms import TrackerUserChangeForm, TrackerUserCreationForm

# Register your models here.



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
