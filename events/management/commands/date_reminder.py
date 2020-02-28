from django.core.management.base import BaseCommand
from django.core.mail import EmailMessage

from events.models import Date
from django.contrib.auth.models import User

class Command(BaseCommand):
    help = "Manages the tasks for sending reminders for dates with need for action"

    def handle(self, *args, **kwargs):
        tbfs = User.objects.filter(groups__name__in=["Technical Operations"])
        for tbf in tbfs:
            tbf_dates = Date.objects.filter(event__responsibles = tbf)
            tbf_dates_critical = {}
            for date in tbf_dates:
                if date._traffic_light() == 'orange' or date._traffic_light() == 'red':
                    if date.event.id not in tbf_dates_critical.keys():
                        tbf_dates_critical[date.event.id] = date
            mail_content = "Für die folgenden Gutachten besteht Handlungsbedarf:<br><br>Gutachten / Windpark <br><br>"
            for date in tbf_dates_critical.values():
                url = 'https://success-map.deutsche-windtechnik.com'+date.event.get_absolute_url()
                date_str =  " / ".join(["<a href="+url+">"+date.event.title+"</a>", date.turbine.wind_farm.name+"<br>"])
                mail_content += date_str
            if tbf_dates_critical:
                headline = "Success Map: tägliche Gutachten-Erinnerung"
                recipient = str(tbf.email)
                mail = EmailMessage(headline, mail_content, 'success-map@deutsche-windtechnik.com', [recipient])
                mail.content_subtype = "html"
                mail.send()