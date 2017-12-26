import datetime
import pytz
import json


from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.core.urlresolvers import reverse
from django.shortcuts import render, redirect
from django.contrib import messages
from django.core.urlresolvers import reverse_lazy
from django.http import HttpResponseRedirect
from django.http import QueryDict
from django.views.generic.edit import FormView
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.messages.views import SuccessMessageMixin
from tracker.models import (
    Event, User, Team, Status, Type, SubType, Ticket, LabelValue, LabelTag
    )
from tracker.forms import (
    EventForm, TeamEventForm, TrackerUserCreationForm
    )
from django.contrib.auth.forms import UserCreationForm
from datetime import date
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.views.generic.edit import CreateView
from django.views.decorators.csrf import csrf_exempt


def localtime_to_utc(time):
    local = pytz.timezone("Asia/Manila")
    local_dt = local.localize(time, is_dst=None)
    utc_dt = local_dt.astimezone (pytz.utc)
    return utc_dt

def create_event(form):
    # Individual Event only. NEXT TODO: Group Event for multiple users
    # check whether it's valid:
    if form.is_valid():
        # process the data in form.cleaned_data as required
        # Status.objects.all()[0]
        # status = form.cleaned_data['status']
        status = Status.objects.get(default=True)
        date_due = form.cleaned_data['date_due']
        agent = form.cleaned_data['agent']
        task_type = form.cleaned_data['task_type']
        # task_sub_type = SubType.objects.get_or_none(pk=request.POST.get('task_sub_type'))
        # Ticket Check Block
        # Creates a ticket if it does not exist
        unique_identifier = form.cleaned_data['unique_identifier']
        ticket_name = form.cleaned_data['ticket_name']
        # Combine Received Date and time -> ToDo : Edit form to pass both Datetime (datetime-local)
        received = form.cleaned_data['received']
        if Ticket.objects.filter(unique_identifier=unique_identifier).exists():
            ticket_name = Ticket.objects.get(unique_identifier=unique_identifier)
        else:
            ticket = Ticket.objects.create(
                name = ticket_name,
                unique_identifier = unique_identifier,
                status = status,
                agent = agent
                )
        quantity = form.cleaned_data['quantity']
        team = form.cleaned_data['team']
        event = Event.objects.create(
            status=status,
            date_due=date_due,
            agent=agent,
            task_type=task_type,
            unique_identifier=unique_identifier,
            ticket_name=ticket_name,
            quantity=quantity,
            team=team,
            received=received,
        )
        return event
    else:
        pass

def create_label(request, event_id):
    #Get Values from request
    new_tag = request.POST.get('label-tag')
    new_value = request.POST.get('label-value')
    print new_tag
    print new_value
    event = Event.objects.get(pk=event_id)
    # If tag submitted does not exist, create it else select existing tag
    if not LabelTag.objects.filter(name=new_tag).exists():
        tag = LabelTag.objects.create(
            name=new_tag,
            )
        tag.event.add(event)
    else:
        tag = LabelTag.objects.get(name=new_tag)
        tag.event.add(event)
    # Create value linked to selected tag
    label = LabelValue.objects.create(
        value=new_value,
        tag=tag,
        )
    label.event.add(event)
    return label
    

def start_event(event, new_status):
    # POST request requirements:
    # event -> key of event
    # activity -> key of status
    print new_status.name
    event.status = new_status
    print event.status
    print "Activity detected is: " + new_status.name
    event.save()

def stop_event(event, new_status):
    # POST request requirements:
    # event -> key of event
    # activity -> key of status
    event.status = new_status
    event.save()

def pause_event(event, new_status):
    # POST request requirements:
    # event -> key of event
    # activity -> key of status
    event.status = new_status
    event.save()


def login_view(request):
    if request.user.is_authenticated():
        return redirect(reverse('home'))
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            username = request.POST['username']
            password = request.POST['password']
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                return redirect(reverse('home'))
            else:
                print 'Invalid credentials'
    else:
        form = AuthenticationForm()

    return render(request, 'tracker/theme/login.html', {'form': form})

@csrf_exempt
def register(request):
    if request.method == 'POST':
        form = TrackerUserCreationForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            raw_password = form.cleaned_data.get('password1')
            team = form.cleaned_data.get('team')
            email = form.cleaned_data.get('email')
            first_name = form.cleaned_data.get('first_name')
            last_name = form.cleaned_data.get('last_name')
            form.save()
            user = authenticate(username=username, password=raw_password)

            login(request, user)
            return redirect('home')
        else:
            print form.errors
    else:
        form = UserCreationForm()
    teams = Team.objects.all()
    return render(request, 'tracker/theme/register.html', {'form': form, 'teams': teams})

@login_required(login_url='/login/')
def logout_view(request):
    try:
        logout(request)

    except Exception as e:
        print "%s: %s" % (e, request.user)

    return redirect('/login')


# Create your views here.
@login_required(login_url='/login/')
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
    paginator = Paginator(events_list, 10)
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
            'idx': None,
        }
    return render(request, 'tracker/home2.html', context)

@login_required(login_url='/login/')    
def track(request):
    if request.method == 'POST':
        status_data = dict(request.POST)
        event_dict = {}
        reference_status = None
        action_status = None
        #Get Events that needs to be changed
        for i in range(0,len(status_data['event'])):
            event = Event.objects.filter(pk = status_data['event'][i])[0]
            if int(event.status.id) != int(status_data['status'][i]):
                action_status = int(status_data['status'][i])
                reference_status = int(event.status.id)
                event_dict[event] = int(status_data['status'][i])
        
        if request.POST.getlist('checks'):
            for event_id in request.POST.getlist('checks'):
                event = Event.objects.filter(pk = event_id)[0]
                if reference_status == int(event.status.id):
                    event_dict[event] = action_status
        
        for event, status in event_dict.items():
                new_status = Status.objects.get(pk=status)
                if new_status.start_event:
                    start_event(event, new_status)
                elif new_status.stop_event:
                    stop_event(event, new_status)
                elif new_status.pause_event:
                    pause_event(event, new_status)
    form = EventForm()
    events_list = Event.objects.filter(agent=request.user).order_by('-timestamp_updated', 'status')
    page = request.GET.get('page', 1)
    paginator = Paginator(events_list, 10)
    try:
        events = paginator.page(page)
    except PageNotAnInteger:
        events = paginator.page(1)
    except EmptyPage:
        events = paginator.page(paginator.num_pages)
    status_start = Status.objects.filter(start_event=True)
    status_stop = Status.objects.filter(stop_event=True)
    status_pause = Status.objects.filter(pause_event=True)
    statuses = Status.objects.all()
    teams = Team.objects.order_by('id')
    users = User.objects.order_by('username')
    types = Type.objects.order_by('id')
    data = {
        'teams': teams,
        'users': users,
        'types': types,
        'statuses': statuses,
        }
    context = {
            'form': form,
            'events': events,
            'status_start': status_start,
            'status_stop': status_stop,
            'status_pause': status_pause,
            'teams': teams,
            'users': users,
            'parent_page': 'home',
            'idx': None,
            'data': data,
        }
    return render(request, 'tracker/theme/track.html', context)
# Fix users_all - should be consistent with all views
def team(request, team_id):
    #Table Actions using POST
    if request.method == 'POST':
        if request.POST.get('action') == 'start':
            start_event(request)
        elif request.POST.get('action   ') == 'stop':
            stop_event(request)
        elif request.POST.get('action') == 'pause':
            pause_event(request)
    events_list = Event.objects.filter(
        team=team_id).order_by('-timestamp_updated', 'status')
    page = request.GET.get('page', 1)
    paginator = Paginator(events_list, 10)
    try:
        events = paginator.page(page)
    except PageNotAnInteger:
        events = paginator.page(1)
    except EmptyPage:
        events = paginator.page(paginator.num_pages)
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

@login_required(login_url='/login/')
def user(request, user_id):
    events_list = Event.objects.filter(
        agent=user_id).order_by('-timestamp_updated', 'status')
    page = request.GET.get('page', 1)
    paginator = Paginator(events_list, 10)
    try:
        events = paginator.page(page)
    except PageNotAnInteger:
        events = paginator.page(1)
    except EmptyPage:
        events = paginator.page(paginator.num_pages)
    # Status Change variables
    status_start = Status.objects.filter(start_event=True)
    status_pause = Status.objects.filter(pause_event=True)
    status_stop = Status.objects.filter(stop_event=True)
    team = Team.objects.get(user=user_id)
    teams = Team.objects.order_by('id')
    user = User.objects.get(pk=user_id)
    users = User.objects.order_by('username')
    initial_dict ={
        'team': user.team.id,
        'agent': user.id
        }
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
            'parent_object': user,
            'id' : user.id,
        }
    return render(request, 'tracker/theme/account.html', context)

@login_required(login_url='/login/')  
def event(request, event_id):
    #Table Actions using POST
    # ToDo: Create own views for table action....
    # Too repetitive
    # Then Best practice: Convert all views to Generic View
    print request.POST
    if request.method == 'POST':
        if request.POST.get('action') == 'start':
            start_event(request)
        elif request.POST.get('action') == 'stop':
            stop_event(request)
        elif request.POST.get('action') == 'pause':
            pause_event(request)
        elif request.POST.get('action') == 'add-label':
            create_label(request, event_id)
    form = EventForm()
    event = Event.objects.get(pk=event_id)
    labels = {}
    for label_value in LabelValue.objects.filter(event=event_id):
        labels[label_value.tag.name] = label_value.value
    status_start = Status.objects.filter(start_event=True)
    status_stop = Status.objects.filter(stop_event=True)
    status_pause = Status.objects.filter(pause_event=True)
    teams = Team.objects.order_by('id')
    users = User.objects.order_by('username')
    types = Type.objects.order_by('id')
    data = {
        'teams': teams,
        'users': users,
        'types': types,
        }
    context = {
            'form': form,
            'event': event,
            'status_start': status_start,
            'status_stop': status_stop,
            'status_pause': status_pause,
            'teams': teams,
            'users': users,
            'parent_page': 'home',
            'idx': None,
            'data': data,
            'labels': labels,
        }
    return render(request, 'tracker/theme/event.html', context)
    
# DELETE THIS? NO MORE USE
def new(request):
    if request.method == 'GET':
        #Get the previous page the new request was created
        referrer = request.META['HTTP_REFERER'].split('/')
        parent_page = referrer[3]
        #Get Default Status
        status = Status.objects.get(default=True)
        initial_dict = {
            'status': status.id,
        }
        #If it is from the home page, throw a basic empty EventForm
        if not parent_page or parent_page == 'event':
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
        if parent_page == 'team' or parent_page == 'user':
            parent_object = Team.objects.get(pk=parent_id)
            if len(request.POST.getlist('agent')) > 1:
                #BAD Practice! Modifying the request! :(
                agents = list(request.POST.getlist('agent'))
                request.POST = request.POST.copy()
                for agent in agents:
                    request.POST['agent']=agent
                    form = EventForm(request.POST)
                    
                    if form.is_valid():
                        event = create_event(form)            
                    else:
                        print form.errors
                        messages.error(request, "Please correct the errors below and resubmit.")
                        if parent_page == 'team':
                            return render(request, 'tracker/theme/track.html', {'form': form})
                        elif parent_page == 'user':
                            return render(request, 'tracker/user.html', {'form': form})

                redirect_url = 'event'
                return redirect(redirect_url, event_id=event.id)
            
            else:
                form = EventForm(request.POST)
        #Error if not user or team
                if form.is_valid():
                    event = create_event(form)            
                    redirect_url = 'event'
                    return redirect(redirect_url, event_id=event.id)
                else:
                    print form.errors
                    messages.error(request, "Please correct the errors below and resubmit.")
                    if parent_page == 'team':
                        return render(request, 'tracker/theme/track.html', {'form': form})
                    elif parent_page == 'user':
                        return render(request, 'tracker/user.html', {'form': form})

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