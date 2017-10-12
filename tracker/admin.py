from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from tracker.models import Event, User, Team


# Register your models here.
@admin.register(User)
class UserAdmin(UserAdmin):
    pass
admin.site.register(Event)
admin.site.register(Team)