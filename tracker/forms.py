import datetime
import pytz

from django import forms
from django.forms import ModelForm
from tracker.models import Event, User, Team, Type
from crispy_forms.helper import FormHelper
from django.core.urlresolvers import reverse
from crispy_forms.layout import Submit, Layout, Div, Button, Fieldset
from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from django.forms.extras.widgets import SelectDateWidget
from django.utils.timezone import now
from django.db.models import Q

# Make dynamic field for Type form
# DRY
# Inherit Forms from EventForm!

# Custom Time function coz i can't set initial time in form using HTML5 type datetime-local
# and time :( I can only set date T_T
def get_time():
    local_tz = pytz.timezone('Asia/Manila')
    utc_dt = datetime.datetime.now()
    local_dt = utc_dt.replace(tzinfo=pytz.utc).astimezone(local_tz)
    return local_tz.normalize(local_dt).strftime("%H:%M")

class EventForm(ModelForm):
    date_due = forms.DateTimeField(required=True, input_formats=['%Y-%m-%dT%H:%M'])
    received = forms.DateTimeField(required=True, input_formats=['%Y-%m-%dT%H:%M'])
    class Meta:
        model = Event
        fields = ['task_type', 'agent', 'team',
                    'unique_identifier', 'ticket_name', 'quantity', 'date_due', 'received']
        exclude =('timestamp_end', 'timestamp_pause','duration','status')
        labels = {
            "unique_identifier": "Ticket Link/ID"
        }
    
    def __init__(self, *args, **kwargs):
        super(EventForm, self).__init__(*args, **kwargs)
         #Labels
        my_field_text= [
            # (field_name, Field title label, Detailed field description)
            ('unique_identifier', 'Ticket Link/ID', ''),
         ]
        for x in my_field_text:
            self.fields[x[0]].label=x[1]
            self.fields[x[0]].help_text=x[2]
        # Set layout for fields.
        self.helper = FormHelper(self)
        self.helper.layout = Layout(
            Div(
                Div('team', css_class="col-sm-10"),
                css_class = 'row'
            ),
            Div(
                Div('task_type', css_class="col-sm-10"),
                css_class = 'row'
            ),
            Div(
                Div('agent', css_class="col-sm-10"),
                css_class = 'row'
            ),
            Div(
                Div('unique_identifier', css_class="col-sm-10"),
                css_class = 'row'
            ),
            Div(
                Div('ticket_name', css_class="col-sm-10"),
                css_class = 'row'
            ),
            Div(
                Div('date_due', css_class="col-sm-10"),
                css_class = 'row'
            ),
            Div(
                Div('quantity', css_class="col-sm-10"),
                css_class = 'row'
            ),
            Div(
                Div('received_date', css_class="col-sm-10"),
                css_class = 'row'
            ),
            Div(
                Div('received_time', css_class="col-sm-10"),
                css_class = 'row'
            ),
            Submit('submit', u'Submit', css_class='btn btn-success'),
        )
        self.helper.form_action = reverse('new')
        self.helper.form_tag = False

    def clean(self):
        cleaned_data = super(EventForm, self).clean()
        team = cleaned_data.get("team")
        task_type = cleaned_data.get("task_type")
        try:
            if task_type.parent_team != team:
                print task_type
                print team
                raise forms.ValidationError(
                    "Invalid Task Type for Team"
                    )
        except AttributeError:
            raise forms.ValidationError("No Task Type Selected")
        return cleaned_data
    
class TeamEventForm(EventForm):
    team = forms.ModelChoiceField(Team)
    date_due = forms.DateField(widget=forms.TextInput(
        attrs={'type' : 'date'}), label='Date Due', initial=datetime.date.today)

    def __init__(self, *args, **kwargs):
        super(TeamEventForm, self).__init__(*args, **kwargs)
        team_id = self.initial['team']
        team_object = Team.objects.get(pk=team_id)
        print team_object, team_id
        self.fields['team'].widget.attrs['initial'] = team_id
        self.fields['team'].widget.attrs['readonly'] = True
        self.fields['task_type'].queryset = Type.objects.filter(Q(parent_team=team_id) | Q(parent_team__name='Others'))
        self.fields['agent'].queryset = User.objects.filter(team=team_id)
        self.fields['team'].queryset = Team.objects.filter(Q(pk=team_id) | Q(name='Others'))

class TrackerUserCreationForm(UserCreationForm):
    
    class Meta(UserCreationForm.Meta):
        model = User
        fields = ("username", "password1", "password2", "team", "first_name", "last_name", "email")
        
    error_message = UserCreationForm.error_messages.update({
        'duplicate_username': 'This username has already been taken.'
    })

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