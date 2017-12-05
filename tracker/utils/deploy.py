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
            'team_code': 'REP',
            'tasks': [
                ['AdHoc', 'ADHOC'],
                ['Insights Deck', 'INSDE'],
                ['Insights QBR', 'INSQBR'],
                ['Insights Queries', 'INSQRY'],
                ['Internal Work', 'INWRK'],
                ['Pixel Split', 'PXSPLT'],
                ['Report Adjustment', 'REPADJ'],
                ['Report Request', 'REPREQ'],
                ['Report Setup', 'REPREQ'],
                ['Scheduled Report', 'SCHREP'],
                ['Support Request', 'SUPREQ'],
            ],
        },
        'Mapping': {
            'team_code': 'MAP',
            'tasks': [
                ['AdHoc', 'ADHOC'],
                ['Adjustment', 'ADJ'],
                ['Discrepancy Investigation', 'DSCRINV'],
                ['DSP Check', 'DSPCHK'],
                ['Manual Upload', 'MANUPL'],
                ['New Request', 'NEWREQ'],
                ['Pipeline Investigation', 'PIPINV'],
            ],
        },
        'Inventory Quality': {
            'team_code': 'IQ',
            'tasks': [
                ['Review', 'REVIEW'],
                ['New Request', 'NEWREQ'],
                ['QA', 'QA'],
                ['Setup', 'STP'],
            ],
        },
        'Screens': {
            'team_code': 'SCR',
            'tasks': [
                ['New Request', 'NEWREQ'],
                ['Kickback', 'KCKBCK'],
                ['New Report', 'NEWREP'],
                ]
        },
        'Others': {
            'team_code': 'OTH',
            'tasks': [
                ['Admin', 'ADMIN'],
                ['Assist', 'ASST'],
                ['Audit', 'AUDT'],
                ['Buddy QA', 'BDYQA'],
                ['Client Call', 'CLIECLL'],
                ['Coaching', 'CCHING'],
                ['Cross Utilization', 'XUTIL'],
                ['Documentation', 'DOCU'],
                ['QA', 'QA'],
                ['Special Projects', 'SPPROJ'],
                ['System Downtime', 'DWNTME'],
                ['Team Meeting', 'TMEET'],
                ['Client Training', 'CLITRN'],
                ['Internal Training', 'INTTRN'],
                ]
        },
    }
    
    for team in team_dict:
        Team.objects.create(
            name=team,
            team_code=team_dict[team]['team_code'],
            )
        # Create Tasks 
        for task in team_dict[team]['tasks']:
            Type.objects.create(
                name=task[0],
                parent_team=Team.objects.get(name=team),
                code=task[1],
                )
    
    