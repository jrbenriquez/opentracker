from django.forms import ModelForm
from tracker.models import Event

class EventForm(ModelForm):
    class Meta:
        model = Event
        fields = ['team', 'agent', 'task_type', 'task_sub_type',
                    'ticket_link', 'ticket_name', 'quantity']