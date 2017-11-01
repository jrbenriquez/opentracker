from django.shortcuts import render
from django.contrib import messages
from django.core.urlresolvers import reverse_lazy
from django.http import HttpResponseRedirect
from django.http import QueryDict
from django.views.generic.edit import FormView
from django.contrib.messages.views import SuccessMessageMixin
from tracker.models import Event, User, Team, Status, Type, SubType, Ticket
from tracker.forms import (
    EventForm, TeamEventForm, TrackerUserCreationForm
    )
from django.contrib.auth.forms import UserCreationForm
from datetime import date
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.views.generic.edit import CreateView

def create_event(form):
    # check whether it's valid:
    if form.is_valid():
        # process the data in form.cleaned_data as required
        # Status.objects.all()[0]
        status = form.cleaned_data['status']
        date_due = form.cleaned_data['date_due']
        agent = form.cleaned_data['agent']
        task_type = form.cleaned_data['task_type']
        # task_sub_type = SubType.objects.get_or_none(pk=request.POST.get('task_sub_type'))
        #Ticket Check Block
        # Creates a ticket if it does not exist
        unique_identifier = form.cleaned_data['unique_identifier']
        ticket_name = form.cleaned_data['ticket_name']
        
        if Ticket.objects.filter(unique_identifier=unique_identifier).exists():
            ticket_name = Ticket.objects.get(unique_identifier=unique_identifier)
        else:
            ticket = Ticket.objects.create(
                name = ticket_name,
                unique_identifier = unique_identifier,
                status = status
                )
        quantity = form.cleaned_data['quantity']
        team = form.cleaned_data['team']
        Event.objects.create(
            status=status,
            date_due=date_due,
            agent=agent,
            task_type=task_type,
            unique_identifier=unique_identifier,
            ticket_name=ticket_name,
            quantity=quantity,
            team=team,
        )
    else:
        pass

def start_event(request):
    # POST request requirements:
    # event -> key of event
    # activity -> key of status
    print request.POST.get('activity')
    eventid = request.POST.get('event')
    event = Event.objects.get(pk=eventid)
    event.status = Status.objects.get(pk=request.POST.get('activity'))
    print event.status
    print "Activity detected is: " + request.POST.get('activity')
    event.save()

def stop_event(request):
    # POST request requirements:
    # event -> key of event
    # activity -> key of status
    print request.POST.get('activity')
    eventid = request.POST.get('event')
    event = Event.objects.get(pk=eventid)
    event.status = Status.objects.get(pk=request.POST.get('activity'))
    event.duration = event.get_duration()
    event.save()

def pause_event(request):
    # POST request requirements:
    # event -> key of event
    # activity -> key of status
    print request.POST.get('activity')
    eventid = request.POST.get('event')
    event = Event.objects.get(pk=eventid)
    event.status = Status.objects.get(pk=request.POST.get('activity'))
    event.duration = event.get_duration()
    event.save()

# Create your views here.
def home(request):
    #Table Actions using POST
    if request.method == 'POST':
        if request.POST.get('action') == 'start':
            start_event(request)
        elif request.POST.get('action') == 'stop':
            stop_event(request)
        elif request.POST.get('action') == 'pause':
            pause_event(request)
    form = EventForm()
    events_list = Event.objects.order_by('-timestamp_updated', 'status')
    page = request.GET.get('page', 1)
    paginator = Paginator(events_list, 25)
    try:
        events = paginator.page(page)
    except PageNotAnInteger:
        events = paginator.page(1)
    except EmptyPage:
        events = paginator.page(paginator.num_pages)
    status_start = Status.objects.filter(start_event=True)
    status_stop = Status.objects.filter(stop_event=True)
    status_pause = Status.objects.filter(pause_event=True)
    teams = Team.objects.order_by('id')
    users = User.objects.order_by('username')
    context = {
            'form': form,
            'events': events,
            'status_start': status_start,
            'status_stop': status_stop,
            'status_pause': status_pause,
            'teams': teams,
            'users': users,
            'parent_page': 'home',
            'idx': None
        }
    return render(request, 'tracker/home.html', context)
# Fix users_all - should be consistent with all views
def team(request, team_id):
    #Table Actions using POST
    if request.method == 'POST':
        if request.POST.get('action') == 'start':
            start_event(request)
        elif request.POST.get('action') == 'stop':
            stop_event(request)
        elif request.POST.get('action') == 'pause':
            pause_event(request)
    events = Event.objects.filter(
        team=team_id).order_by('-timestamp_updated', 'status')
    status_start = Status.objects.filter(start_event=True)
    status_pause = Status.objects.filter(pause_event=True)
    status_stop = Status.objects.filter(stop_event=True)
    team = Team.objects.get(pk=team_id)
    teams = Team.objects.order_by('id')
    users_all = User.objects.order_by('username')
    users = User.objects.filter(team=team_id)
    initial_dict = {
            'team': team.id,
    }
    form = TeamEventForm(initial = initial_dict)
    context = {
            'form': form,   
            'events': events,
            'status_start': status_start,
            'status_stop': status_stop,
            'status_pause': status_pause,
            'team': team,
            'teams': teams,
            'users' : users,
            'parent_page': 'team',
            'id' : team.id,
            'users_all' : users_all
        }
    return render(request, 'tracker/team.html', context)

def user(request, user_id):
     #Table Actions using POST
    if request.method == 'POST':
        if request.POST.get('action') == 'start':
            start_event(request)
        elif request.POST.get('action') == 'stop':
            stop_event(request)
        elif request.POST.get('action') == 'pause':
            pause_event(request)
    events = Event.objects.filter(
        agent=user_id).order_by('-timestamp_updated', 'status')
    # Status Change variables
    status_start = Status.objects.filter(start_event=True)
    status_pause = Status.objects.filter(pause_event=True)
    status_stop = Status.objects.filter(stop_event=True)
    team = Team.objects.get(user=user_id)
    teams = Team.objects.order_by('id')
    user = User.objects.get(pk=user_id)
    users = User.objects.order_by('username')
    context = {
            'events': events,
            'status_start': status_start,
            'status_pause': status_pause,
            'status_stop': status_stop,
            'teams': teams,
            'users': users,
            'team': team,
            'user' : user,
            'parent_page': 'user',
            'id' : user.id
        }
    return render(request, 'tracker/user.html', context)

def event(request, event_id):
    #Table Actions using POST
    print request.POST
    if request.method == 'POST':
        if request.POST.get('action') == 'start':
            start_event(request)
        elif request.POST.get('action') == 'stop':
            stop_event(request)
        elif request.POST.get('action') == 'pause':
            pause_event(request)
    event = Event.objects.get(pk=event_id)
    status_start = Status.objects.filter(start_event=True)
    status_pause = Status.objects.filter(pause_event=True)
    status_stop = Status.objects.filter(stop_event=True)
    context = {
        'event': event,
        'status_start': status_start,
        'status_pause': status_pause,
        'status_stop': status_stop,
    }
    
    return render(request, 'tracker/event.html', context)
    

def new(request):
    if request.method == 'GET':
        #Get the previous page the new request was created
        referrer = request.META['HTTP_REFERER'].split('/')
        parent_page = referrer[3]
        #If it is from the home page, throw a basic empty EventForm
        if not parent_page:
            form = EventForm()
            context = {
                        'form': form,
                        'parent_page': parent_page,
            }
        #Else load the necessary initial values to the form
        else:
            #Get the specific id of requestor
            parent_id = referrer[4]
            if parent_page == 'team':
                parent_object = Team.objects.get(pk=parent_id)
                initial_dict ={
                        'team': parent_object.id
                        
                }
                form = TeamEventForm(initial=initial_dict)
            elif parent_page == 'user':
                parent_object = User.objects.get(pk=parent_id)
                initial_dict ={
                        'team': parent_object.team.id,
                        'agent': parent_object.id
                        
                }
                form = TeamEventForm(initial=initial_dict)
            #Error if not user or team
            context = {
                    'form': form,
                    'parent_page': parent_page,
                    'parent_object' : parent_object,
                    'id' : parent_object.id
                    
                }
        print "RENDERIIINGs"
        return render(request, 'tracker/new_event.html', context)

def new_submit(request, parent_page):
    print request.method
    if request.method == 'POST':
        parent_id = request.POST.get('team')
        if parent_page == 'team':
            parent_object = Team.objects.get(pk=parent_id)
            form = TeamEventForm(request.POST, initial={'team': parent_id})
        elif parent_page == 'user':
            parent_object = User.objects.get(pk=parent_id)
        #Error if not user or team
        print parent_id
        if form.is_valid():
            create_event(form)
            return HttpResponseRedirect('/')
        else:
            messages.error(request, "Please correct the errors below and resubmit.")
            return render(request, 'tracker/new_event.html', {'form': form})


class NewUserView(CreateView):
    template_name = 'tracker/user/user_new.html'
    form_class = TrackerUserCreationForm
    success_url = '/'
        
class AjaxTemplateMixin(object):
    def dispatch(self, request, *args, **kwargs):
        if not hasattr(self, 'ajax_template_name'):
            split = self.template_name.split('.html')
            split[-1] = '_inner'
            split.append('.html')
            self.ajax_template_name = ''.join(split)
        if request.is_ajax():
            self.template_name = self.ajax_template_name
        return super(AjaxTemplateMixin, self).dispatch(request, *args, **kwargs)

class EventFormView(SuccessMessageMixin, AjaxTemplateMixin, FormView):
    template_name = 'tracker/new_event.html'
    form_class = EventForm
    success_url = reverse_lazy('new')
    success_message = "Way to go!"