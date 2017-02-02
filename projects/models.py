import datetime

from django.utils import timezone
from django.db import models
from django.conf import settings


# Create your models here.
class Company(models.Model):
    """company data
    """
    name = models.CharField(max_length=255)
    notes = models.TextField(blank=True, null=True)


class Project(models.Model):
    """Project data
    """
    account = models.ForeignKey(settings.AUTH_USER_MODEL)
    company = models.ForeignKey('Company')

    name = models.CharField(max_length=500)
    notes = models.TextField(blank=True, null=True)

    def __str__(self):
        return '[{}] {}'.format(self.company.name, self.account)


class ProjectMember(models.Model):
    account = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='member')
    project = models.ForeignKey('Project')

    def __str__(self):
        return '[{}] {}'.format(self.project.name, self.account)

    class Meta:
        unique_together = ('account', 'project')


class Log(models.Model):
    member = models.ForeignKey('ProjectMember')
    memo = models.TextField(blank=False, null=False)
    is_approved = models.BooleanField(default=False)
    start = models.DateTimeField(blank=False, null=False)
    end = models.DateTimeField(blank=True, null=True)

    @property
    def seconds(self):
        """Get the difference between start and end
        """
        end = self.end or timezone.now()
        result = end - self.start
        return result.seconds

    @property
    def log(self):
        """Get the time spent for the log
        """
        return str(datetime.timedelta(seconds=self.seconds))
