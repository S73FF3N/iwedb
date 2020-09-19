from django.core.management.base import BaseCommand
from django.core.mail import EmailMessage
from django.utils import translation
from django.utils.translation import ugettext as _
from django.core.exceptions import ObjectDoesNotExist

from events.models import Date
from django.contrib.auth.models import User

from datetime import date

class Command(BaseCommand):
    help = "Manages the tasks for sending reminders for dates with need for action"

    def handle(self, *args, **kwargs):
        translation.activate('de')
        tbfs = User.objects.filter(groups__name__in=["Technical Operations"])
        for tbf in tbfs:
            tbf_dates = Date.objects.filter(event__responsibles = tbf)
            tbf_dates_critical = {}
            for d in tbf_dates:
                if d._traffic_light() == 'orange' or d._traffic_light() == 'red':
                    if d.event.id not in tbf_dates_critical.keys():
                        tbf_dates_critical[d.event.id] = d
            mail_content = "Für die folgenden Gutachten besteht Handlungsbedarf:<br><br>Gutachten / Windpark <br><br>"
            for d in tbf_dates_critical.values():
                url = 'https://success-map.deutsche-windtechnik.com'+d.event.get_absolute_url()
                try:
                    wind_farm_name = d.turbine.wind_farm.name
                except ObjectDoesNotExist:
                    wind_farm_name = "Kein Windpark angegeben"
                date_str =  " / ".join(["<a href="+url+">"+ _(d.event.title) +"</a>", wind_farm_name +"<br>"])
                mail_content += date_str
            if tbf_dates_critical and date.today().weekday() == 0:
                headline = "Success Map: wöchentliche Gutachten-Erinnerung"
                recipient = str(tbf.email)
                mail = EmailMessage(headline, mail_content, 'success-map@deutsche-windtechnik.com', [recipient])
                mail.content_subtype = "html"
                mail.send()
