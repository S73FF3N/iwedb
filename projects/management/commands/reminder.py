from datetime import datetime

from django.core.management.base import BaseCommand
from django.core.mail import EmailMessage

from projects.models import Reminder, Project

class Command(BaseCommand):
    help = "Manages the tasks for sending reminders"

    def handle(self, *args, **kwargs):
        todays_reminder = Reminder.objects.filter(date=datetime.today())
        for r in todays_reminder:
            project = Project.objects.get(id=r.object_id)
            mail = EmailMessage(
                " ".join(['Reminder: Project',str(project.name)]),
                " ".join(['The reminder with the following content was set by',r.created_by.first_name,r.created_by.last_name,'on',str(r.created.date()),'.','<br><br>',r.text,'<br><br>','http://success-map.deutsche-windtechnik.com'+project.get_absolute_url()]),
                'success-map@deutsche-windtechnik.com',
                [str(r.recipient.email)],
                )
            mail.content_subtype = "html"
            mail.send()
        #self.stdout.write(str(project.name))