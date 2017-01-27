import datetime

from django.contrib.auth.mixins import LoginRequiredMixin
from django.utils import timezone

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
            member = ProjectMember.objects.get(account=user,
                                               project=project)
            Log.objects.create(member=member,
                               start=timezone.now(),
                               memo=memo)

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
