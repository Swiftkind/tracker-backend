import datetime

from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.mail import EmailMultiAlternatives
from django.template import Context
from django.template.loader import get_template
from django.utils import timezone

from accounts.models import Account
from .models import (
                        Log,
                        Project,
                        ProjectMember
                    )


class AdminLoginRequiredMixin(LoginRequiredMixin):

    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_superuser:
            return self.handle_no_permission()
        return super(LoginRequiredMixin, self).dispatch(request, *args, **kwargs)


class TimeLogMixin(object):
    """Class to manage logging
    """

    def is_logged(self, user):
        """Check if user is already logging
        """
        is_log = Log.objects.filter(member__account=user,
                                    end=None)
        return is_log.exists()

    def time_out(self, user):
        """User time out
        """

        if self.is_logged(user):
            logs = Log.objects.filter(member__account=user, end=None)
            logs.update(end=timezone.now())

    def time_in(self, user, project, memo):
        """User time in
        """

        if self.is_logged(user):
            self.time_out(user)
        else:
            try:
                member = ProjectMember.objects.get(account=user,
                                                   project=project)
                Log.objects.create(member=member,
                                   start=timezone.now(),
                                   memo=memo)
            except ProjectMember.DoesNotExist:
                raise ProjectMember.DoesNotExist('No access for the project')

    def current_logged(self, user):
        """Get user current log
        """
        logs = Log.objects.filter(member__account=user,
                                    end=None)
        if logs:
            return logs.first()

        return None


class TimeSheetMixin(object):
    """Manage time sheet
    """

    def user_projects(self, user):
        """List user projects
        """
        projects = ProjectMember.objects.filter(account=user)
        return Project.objects.filter(id__in=projects.values_list('project__id', flat=True))

    def total_hours(self, queryset):
        """Get total hours
        """
        seconds = 0
        for log in queryset:
            seconds += log.seconds

        return str(datetime.timedelta(seconds=seconds))

    def week_date(self):
        """We the range date for the week
        """
        date = timezone.now().today()
        current_date = date
        monday = date - datetime.timedelta(days=date.weekday())
        return {
            'start_date': monday.date(),
            'current_date': current_date
        }

    def user_timesheet(self, user, project=None):
        """Check user timesheet
        """

        logs = Log.objects.filter(member__account=user)

        if project:
            logs = logs.filter(member__project=project)

        return logs

class AddMemberMixin(object):
    """manages sending of invites and adding user to project
    """
    def add_to_project(self, data):
        """add to project
        """
        account = Account.objects.get(email=data['member'])
        project = Project.objects.get(id=data['id'])
        return ProjectMember.objects.create(account=account, project=project)


    def send_invite(self, data):
        """send invite
        """
        subject = "SwiftTracker Project Invitation"
        html = get_template('projects/invitation.html')
        admin = Account.objects.get(id=data['account'])

        context_data = Context({
                    'admin': admin,
                    'project': data['name'],
                    'url': data['url']
                    })

        email_to = data['member']
        html_content = html.render(context_data)
        msg = EmailMultiAlternatives(subject, to=[email_to])
        msg.attach_alternative(html_content, "text/html")
        msg.send()