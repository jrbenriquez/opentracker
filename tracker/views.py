from django.shortcuts import render
from tracker.models import Event, User, Team, Status, Type, SubType, Ticket
from tracker.forms import EventForm
from django.http import HttpResponseRedirect

# Create your views here.
def home(request):
    print request.method
    if request.method == 'POST':
        # create a form instance and populate it with data from the request:
        if request.POST.get('action') == 'start':
            # POST request requirements:
            # event -> key of event
            # activity -> key of status
            print request.POST.get('activity')
            eventid = request.POST.get('event')
            event = Event.objects.get(pk=eventid)
            event.status = Status.objects.get(pk=request.POST.get('activity'))
            event.save()
            
            
            
        elif request.POST.get('action') == 'stop':
            # POST request requirements:
            # event -> key of event
            # activity -> key of status
            print request.POST.get('activity')
            eventid = request.POST.get('event')
            event = Event.objects.get(pk=eventid)
            event.status = Status.objects.get(pk=request.POST.get('activity'))
            event.duration = event.get_duration()
            event.save()
            
        else:
            form = EventForm(request.POST)
            # check whether it's valid:
            if form.is_valid():
                # process the data in form.cleaned_data as required
                # Status.objects.all()[0]
                status = Status.objects.get(pk=request.POST.get('status'))
                timestamp_pause = request.POST.get('timestamp_pause')
                timestamp_end = request.POST.get('timestamp_end')
                date_due = request.POST.get('date_due')
                agent = User.objects.get(pk=request.POST.get('agent'))
                task_type = Type.objects.get(pk=request.POST.get('task_type'))
                task_sub_type = SubType.objects.get(pk=request.POST.get('task_sub_type'))
                #Ticket Check Block
                # Creates a ticket if it does not exist
                ticket_link = request.POST.get('ticket_link')
                ticket_name = request.POST.get('ticket_name')
                
                if Ticket.objects.filter(link=ticket_link).exists():
                    ticket_name = Ticket.objects.get(link=ticket_link)
                else:
                    ticket = Ticket.objects.create(
                        name = ticket_name,
                        link = ticket_link
                        )
                quantity = request.POST.get('quantity')
                team = Team.objects.get(pk=request.POST.get('team'))
                Event.objects.create(
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
    form = EventForm()
    events = Event.objects.order_by('-timestamp_updated', 'status')
    status_start = Status.objects.filter(start_event=True)
    status_stop = Status.objects.filter(stop_event=True)
    teams = Team.objects.all()
    context = {
            'form': form,
            'events': events,
            'status_start': status_start,
            'status_stop': status_stop,
            'teams': teams
        }
    return render(request, 'tracker/home.html', context)