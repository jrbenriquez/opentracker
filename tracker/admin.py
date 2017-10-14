from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from tracker.models import Event, User, Team, Status, Type, SubType, Ticket, Activity


# Register your models here.
@admin.register(User)
class UserAdmin(UserAdmin):
    pass
admin.site.register(Event)
admin.site.register(Team)
admin.site.register(Status)
admin.site.register(Type)
admin.site.register(SubType)
admin.site.register(Ticket)
admin.site.register(Activity)
