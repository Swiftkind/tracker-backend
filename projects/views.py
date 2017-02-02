from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import TemplateView
from django.shortcuts import redirect
from django.urls import reverse
from django.utils import timezone

from rest_framework.response import Response
from rest_framework import viewsets

from accounts.models import Account

from .permissions import AdminPermission
from .mixins import (TimeSheetMixin,
                     TimeLogMixin,
                     AdminLoginRequiredMixin
                    )
from .models import (
                     Project,
                     Company,
                     Log,
                     ProjectMember
                    )
from .serializers import (CompanySerializer,
                          ProjectSerializer,
                          ProjectMemberSerializer,
                          LogSerializer)


class TimeLogTemplateView(LoginRequiredMixin,
                          TimeLogMixin,
                          TimeSheetMixin,
                          TemplateView):
    """User time-in and time-out

    TODO: remove once api is working
    """

    template_name = 'projects/timelog.html'

    def get(self, request):
        today = timezone.now().date()
        user_timesheet = self.user_timesheet(user=request.user)
        timesheet_queryset = user_timesheet.filter(
                                                start__year=today.year,
                                                start__month=today.month,
                                                start__day=today.day
                                            ).order_by('-start')
        week_dates = self.week_date()
        weekly_timesheet = user_timesheet.filter(start__range=[week_dates['start_date'], week_dates['current_date']]).order_by('-start')
        context = {
            'is_logged': self.is_logged(request.user),
            'projects': self.user_projects(request.user),
            'current_logged':  self.current_logged(request.user),
            'today_timelogs': timesheet_queryset,
            'total_hours_today': self.total_hours(timesheet_queryset),
            'weekly_timelogs': weekly_timesheet,
            'weekly_hours': self.total_hours(weekly_timesheet),
            'week_dates': week_dates,
        }
        return self.render_to_response(context)

    def post(self, request):
        post = request.POST
        project = Project.objects.get(id=int(post['project']))

        if 'start' in post:
            self.time_in(user=request.user,
                        memo=post['memo'],
                        project=project)
        else:
            self.time_out(user=request.user)

        return redirect(reverse('timelog'))


class AdminTemplateView(AdminLoginRequiredMixin,
                        TimeLogMixin,
                        TimeSheetMixin,
                        TemplateView):
    """To be remove
    """

    template_name = "projects/timesheet_summary.html"

    def get(self, request):
        """Not recommended script.  Need to add better script here soon.
        """
        users = []
        data = request.GET
        week_dates = self.week_date()
        start = data.get('start', week_dates['start_date'])
        end = data.get('end', week_dates['current_date'].date())
        project = data.get('project', '')
        member = data.get('member', '')
        members = Account.objects.filter(is_superuser=False).order_by('first_name')
        projects = Project.objects.all().order_by('name')

        if member:
            accounts = members.filter(id=member)
        else:
            accounts = members

        for account in accounts:
            user_timesheet = self.user_timesheet(user=account)
            timesheets = user_timesheet.filter(start__range=[start, '{} 23:59:59'.format(end)]).order_by('-start')

            # filter by project
            if project:
                timesheets = timesheets.filter(member__project__id=project)

            account.log = self.total_hours(timesheets)
            account.timesheets = timesheets
            users.append(account)

        return self.render_to_response({
                                        'users': users,
                                        'start': str(start),
                                        'end': str(end),
                                        'projects': projects,
                                        'project_selected': project,
                                        'members': members,
                                        'member': member
                                    })


class CompanyReadOnlyViewSet(viewsets.ReadOnlyModelViewSet):
    """Handle company endpoints
    """

    queryset = Company.objects.all()
    serializer_class = CompanySerializer


class ProjectReadOnlyViewSet(viewsets.ReadOnlyModelViewSet):
    """Handle project readonly endpoints
    """

    queryset = Project.objects.all()
    serializer_class = ProjectSerializer

    def get_queryset(self):
        """Return list of projects by user
        """
        queryset = self.queryset.filter(projectmember__account=self.request.user)
        return queryset


class ProjectMemberReadOnlyViewSet(viewsets.ReadOnlyModelViewSet):

    queryset = ProjectMember.objects.all()
    serializer_class = ProjectMemberSerializer

    def get_queryset(self):
        """Return list of members by project
        """
        # Get the projects access by request.user
        projects = Project.objects.filter(projectmember__account=self.request.user)
        queryset = self.queryset.filter(project__in=projects)
        return queryset


class LogReadOnlyViewSet(viewsets.ReadOnlyModelViewSet):
    """Handle log transactions
    """

    queryset = Log.objects.all()
    serializer_class = LogSerializer

    def get_queryset(self):
        """Return list of logs
        """

        if self.request.user.is_superuser is False:
            # Filter by account if request.user is not superuser
            self.queryset = self.queryset.filter(member__account=self.request.user)

        return self.queryset


class LogViewSet(viewsets.ViewSet, TimeLogMixin):
    """Handle timein, timeout and display last timein activity
    """
    serializer_class = LogSerializer

    def current_log(self, request):
        """Return current activity

        method = GET
        """
        serializer = self.serializer_class(self.current_logged(request.user))
        return Response(serializer.data)

    def timelog(self, request):
        """Time-in and Time-out

        method = POST

        data values:
            project - project id
            memo - text, leave blank for timeout
            timein - true or false
        """

        data = request.data
        project = Project.objects.get(id=data['project'])

        if data['timein'] == True:
            self.time_in(user=request.user,
                     project=project,
                     memo=data['memo'])
        else:
            self.time_out(request.user)

        serializer = self.serializer_class(self.current_logged(request.user))
        return Response(serializer.data)
