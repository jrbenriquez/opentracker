from __future__ import unicode_literals

from django.db import models
from django.conf import settings
from django.contrib.auth.models import AbstractUser

from tracker.constants.back_office import BACK_OFFICE_DICT

# Create your models here.
class Team(models.Model):
    name = models.CharField(max_length=20,
                            unique=True)
    team_code = models.CharField(max_length=10,
                            unique=True)
    
    def __str__(self):
        return self.name
        

class Event(models.Model):
    timestamp_start = models.DateTimeField(auto_now_add=True)
    timestamp_pause = models.DateTimeField(blank=True, null=True)
    timestamp_end = models.DateTimeField(blank=True, null=True)
    timestamp_updated = models.DateTimeField(auto_now=True)
    status = models.CharField(max_length=30,
                              choices=BACK_OFFICE_DICT['status'],
                              default=BACK_OFFICE_DICT['status'][0][0],
                              null=True
                              )
    date_due = models.DateTimeField(blank=True, null=True)
    agent = models.ForeignKey(settings.AUTH_USER_MODEL)
    task_type = models.CharField(max_length=30, choices=BACK_OFFICE_DICT['task_types'])
    task_sub_type = models.CharField(max_length=30, choices=BACK_OFFICE_DICT['task_sub_types'])
    ticket_link = models.CharField(max_length=300)
    ticket_name = models.CharField(max_length=100)
    quantity = models.IntegerField()
    team = models.ForeignKey(Team)
    
    def __str__(self):
        return '[%s] %s' % (self.id, self.ticket_name)
    @property
    def get_task_type(self):
        return dict(BACK_OFFICE_DICT['task_types']).get(self.task_type)
    @property
    def get_task_sub_type(self):
        return dict(BACK_OFFICE_DICT['task_sub_types']).get(self.task_sub_type)

    @property
    def get_first_name(self):
        agent = User.objets.get(pk=self.agent)
        return agent.get_first_name
        

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
    

