from django.shortcuts import render
from tracker.models import Event, User, Team
from tracker.forms import EventForm
from django.http import HttpResponseRedirect

from tracker.constants.back_office import BACK_OFFICE_DICT

# Create your views here.
def home(request):
    if request.method == 'POST':
        # create a form instance and populate it with data from the request:
        form = EventForm(request.POST)
        # check whether it's valid:
        if form.is_valid():
            # process the data in form.cleaned_data as required
            status = 'IP'
            timestamp_pause = request.POST.get('timestamp_pause')
            timestamp_end = request.POST.get('timestamp_end')
            date_due = request.POST.get('date_due')
            agent = User.objects.get(pk=request.POST.get('agent'))
            task_type = request.POST.get('task_type')
            task_sub_type = request.POST.get('task_sub_type')
            ticket_link = request.POST.get('ticket_link')
            ticket_name = request.POST.get('ticket_name')
            quantity = request.POST.get('quantity')
            team = Team.objects.get(pk=request.POST.get('team'))
            event = Event.objects.create(
                status=status,
                timestamp_pause=timestamp_pause,
                timestamp_end=timestamp_end,
                date_due=date_due,
                agent=agent,
                task_type=task_type,
                task_sub_type=task_sub_type,
                ticket_link=ticket_link,
                ticket_name=ticket_name,
                quantity=quantity,
                team=team,
            )
            # ...
            # redirect to a new URL:
            return HttpResponseRedirect('/')
        else:
            pass
    # if a GET (or any other method) we'll create a blank form
    else:
        form = EventForm()
        events = Event.objects.all()
        context = {
            'form': form,
            'events': events,
        }
    form = EventForm()
    events = Event.objects.all()
    context = {
            'form': form,
            'events': events,
        }
    return render(request, 'tracker/home.html', context)