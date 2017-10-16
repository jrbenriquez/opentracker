from django.forms import ModelForm
from tracker.models import Event

class EventForm(ModelForm):
    class Meta:
        model = Event
        fields = ['status', 'team', 'agent', 'task_type', 'task_sub_type',
                    'unique_identifier', 'ticket_name', 'quantity']