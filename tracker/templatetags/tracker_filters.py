from django import template


register = template.Library()


@register.filter(name='task_duration')
def task_duration(td, arg='simple'):
    try:
        total_seconds = int(td.total_seconds())
    except AttributeError:
        return 'None'
    hours = total_seconds // 3600
    minutes = (total_seconds % 3600) // 60
    seconds =  ((total_seconds % 3600) % 60)
    if arg == 'simple':
        if hours:
            return '{:02d}:{:02d}:{:02d}'.format(hours, minutes, seconds)
        elif minutes:
            return '{:02d}:{:02d}'.format(minutes, seconds)
        elif seconds:
            return '{:02d}s'.format(seconds)
    elif arg == 'verbose':
        if hours:
            return '{} hours {} minutes {} seconds'.format(hours, minutes, seconds)
        elif minutes:
            return '{} mintes {} seconds'.format(minutes, seconds)
        elif seconds:
            return '{} seconds'.format(seconds)
        
