from tracker.models import Status, Team, Type

def post_deploy_setup():
    # Create Status
    status_dict = {
        'In Progress': {
            'code': 'IP',
            'start_event': True ,
            'pause_event': False,
            'stop_event':  False,
            'default': True,
        },
        'On Hold': {
            'code': 'OH',
            'start_event': False ,
            'pause_event': True,
            'stop_event':  False,
            'default': False,
        },
        'Done': {
            'code': 'D',
            'start_event': False ,
            'pause_event': False,
            'stop_event':  True,
            'default': False,
        },
    }
    
    for status in status_dict:
        Status.objects.create(
            name=status,
            code=status_dict[status]['code'],
            start_event=status_dict[status]['start_event'],
            pause_event=status_dict[status]['pause_event'],
            stop_event=status_dict[status]['stop_event'],
            default=status_dict[status]['default'],
            )
    # Create Team
    team_dict = {
        'Reporting': {
            'team_code': 'REP'
        },
        'Mapping': {
            'team_code': 'MAP'
        }
    }
    
    for team in team_dict:
        Team.objects.create(
            name=team,
            team_code=team_dict[team]['team_code'],
            )
    # Create Tasks 
    task_dict = {
        'Scheduled Report': {
            'parent_team': Team.objects.get(name='Reporting'),
            'code': 'SCHREP',
        }
    }
    
    for task in task_dict:
        Type.objects.create(
            name=task,
            parent_team=task_dict[task]['parent_team'],
            code=task_dict[task]['code'],
            )