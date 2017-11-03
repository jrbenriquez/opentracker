from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as AuthUserAdmin
from tracker.models import Event, User, Team, Status, Type, Ticket, Activity
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
    
class ActivityAdmin(admin.ModelAdmin):
    list_display = ('date', 'event', 'action', 'agent')
    list_display_links = ('date', 'event')
    search_fields = ('event__ticket_name', 'event__unique_identifier', 'agent__first_name', 'agent__username')
    list_per_page = 25

class EventAdmin(admin.ModelAdmin):
    list_display = ('__str__', 'agent', 'status', 'date_due')
    list_display_links = ('__str__', 'agent')
    search_fields = ('status__name', '__str__', 'agent__first_name', 'agent__username')
    list_per_page = 25

admin.site.register(Event, EventAdmin)
admin.site.register(Team)
admin.site.register(Status)
admin.site.register(Type)
admin.site.register(Ticket)
admin.site.register(Activity, ActivityAdmin)
