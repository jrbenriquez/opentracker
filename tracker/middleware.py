from django.utils import timezone

import pytz


class TimezoneMiddleware(object):

    def process_request(self, request):
        tz = 'Asia/Manila'
        timezone.activate(pytz.timezone(tz))