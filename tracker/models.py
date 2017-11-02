from __future__ import unicode_literals

from django.db import models
from django.conf import settings
from django.contrib.auth.models import AbstractUser
from django.db.models.signals import pre_save, post_save
from django.core.exceptions import ObjectDoesNotExist

#Manager
class TrackerManager(models.Manager):

    def get_or_none(self, **kwargs):
        try:
            return self.get(**kwargs)
        except ObjectDoesNotExist:
            return None
# Create your models here.
class Team(models.Model):
    name = models.CharField(max_length=20,
                            unique=True)
    team_code = models.CharField(max_length=10,
                            unique=True)
    
    def __str__(self):
        return self.name
        

class Comment(models.Model):
    
    agent = models.ForeignKey(settings.AUTH_USER_MODEL)
    message = models.CharField(max_length=300)
    timestamp_created = models.DateTimeField(auto_now_add=True)
    timestamp_updated = models.DateTimeField(auto_now =True)


class User(AbstractUser):
    team = models.ForeignKey(Team, null=True)
    
    def __str__(self):
        return self.first_name
    
    def __repr__(self):
        return self.first_name
    
    @property
    def full_name(self):
        return '%s %s' % (self.first_name, self.last_name)
        
class Status(models.Model):
    name = models.CharField(max_length=30)
    code = models.CharField(max_length=10)
    start_event = models.BooleanField(default = True)
    pause_event = models.BooleanField(default = False)
    stop_event = models.BooleanField(default = False)
    default = models.BooleanField(default = False)
    
    def __str__(self):
        return self.name

class Type(models.Model):
    parent_team = models.ForeignKey(Team)
    name = models.CharField(max_length=30)
    code = models.CharField(max_length=10)

    def __str__(self):
        return self.name
    
    @property
    def get_representative_name(self):
        return "%s - %s" % (self.parent_team, self.name)

class SubType(models.Model):
    parent_type = models.ForeignKey(Type)
    name = models.CharField(max_length=30)
    code = models.CharField(max_length=10)
    objects = TrackerManager()
    def __str__(self):
        return self.name

    
class Event(models.Model):
    timestamp_start = models.DateTimeField(auto_now_add=True)
    timestamp_pause = models.DateTimeField(blank=True, null=True)
    timestamp_end = models.DateTimeField(blank=True, null=True)
    timestamp_updated = models.DateTimeField(auto_now=True)
    status = models.ForeignKey(Status)
    date_due = models.DateTimeField(blank=True, null=True)
    agent = models.ForeignKey(settings.AUTH_USER_MODEL)
    task_type = models.ForeignKey(Type)
    unique_identifier = models.CharField(max_length=500)
    ticket_name = models.CharField(max_length=500)
    quantity = models.IntegerField()
    team = models.ForeignKey(Team)
    duration = models.DurationField(null=True, blank=True)
    
    def __str__(self):
        return '[%s] %s - %s' % (self.id, self.ticket_name, self.task_type)
    @property
    def get_first_name(self):
        agent = User.objets.get(pk=self.agent)
        return agent.get_first_name
   
    def get_duration(self, *args, **kwargs):
        # Get all activities related to event
        # Compute for proper time
        start_activity = None
        stop_activity = None
        duration = None
        
        if Activity.objects.filter(event=self.id).exists():
            activity_set = Activity.objects.filter(event=self.id).order_by('date')
            print 'Found Activity! ' + str(len(activity_set)) 
            for activity in activity_set:
                if activity.action.start_event:
                    print 'Saw activity %s' % (activity.action.name)
                    start_activity = activity.date
                    print 'Start: ' + str(start_activity)
                elif activity.action.stop_event or activity.action.pause_event:
                    print 'Saw activity %s' % (activity.action.name)
                    stop_activity = activity.date
                    print 'Stop: ' + str(stop_activity)
                    # If event started with a stop event don't do any calculations 
                    try:
                        latest_duration = stop_activity - start_activity
                        if duration is None:
                            duration = latest_duration
                        else:
                            duration = duration + latest_duration
                        print 'Duration: ' + str(duration)
                    except TypeError:
                        print "No Calculations Done!"
                else:
                    pass
        return duration
        

class Ticket(models.Model):
    name = models.CharField(max_length=500)
    unique_identifier = models.CharField(max_length=300, unique=True)
    status = models.ForeignKey(Status)
    agent = models.ForeignKey(User)
    
    def __str__(self):
        return self.unique_identifier
    
    def get_duration(self):
        events = Event.objects.filter(ticket_name=self.name)
        duration = None
        for event in events:
            if event.duration:
                if duration:
                    duration += event.duration
                else:
                    duration = event.duration
        return duration

class Activity(models.Model):
    date = models.DateTimeField(auto_now_add=True)
    action = models.ForeignKey(Status)
    agent = models.ForeignKey(settings.AUTH_USER_MODEL)
    event = models.ForeignKey(Event)
    ticket = models.ForeignKey(Ticket)
    
    def __str__(self):
        return "%s - %s - %s - %s" %(self.date, self.agent, self.action, self.ticket.name)

def create_activity(sender, **kwargs):
    ''' Create activity when event is changed and compute for duration '''
    event = kwargs['instance']
    if event:
        activity = Activity.objects.create(
            event=kwargs['instance'],
            action=kwargs['instance'].status,
            agent=kwargs['instance'].agent,
            ticket=Ticket.objects.get(unique_identifier = kwargs['instance'].unique_identifier ),
        )
        update_event_duration = Event.objects.filter(pk=event.id).update(
            duration = event.get_duration())
 
def update_ticket_status(sender, **kwargs):
    ''' Update the status of the ticket after an activity is done '''
    activity = kwargs['instance']
    if activity:
        update_ticket = Ticket.objects.filter(
            unique_identifier=activity.event.unique_identifier
        ).update(status = activity.action)
     
post_save.connect(create_activity, sender=Event)
#After saving activity update Ticket status
post_save.connect(update_ticket_status, sender=Activity)