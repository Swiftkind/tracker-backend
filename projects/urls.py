from django.conf.urls import url

from rest_framework import routers

from .views import (
                    TimeLogTemplateView,
                    AdminTemplateView,

                    # endpoints
                    ProjectReadOnlyViewSet,
                    ProjectMemberReadOnlyViewSet,
                    LogViewSet,
                    LogReadOnlyViewSet,
                    CompanyReadOnlyViewSet,
                    AddMemberViewset,
                    ProjectMembersViewset,
                    ProjectsViewset,
                    MemberLogsAPI
                )

urlpatterns = [
    url(r'^timelog', TimeLogTemplateView.as_view(), name='timelog'),
    url(r'^timesheet', AdminTemplateView.as_view(), name='timesheet')
]

# Api endpoints
router = routers.SimpleRouter()
router.register(r'projects', ProjectReadOnlyViewSet)
router.register(r'project-members', ProjectMemberReadOnlyViewSet)
router.register(r'logs', LogReadOnlyViewSet)
router.register(r'company', CompanyReadOnlyViewSet)

api_urlpatterns = router.urls

api_urlpatterns += [
    url(r'^timelog/', LogViewSet.as_view({
        'get': 'current_log',
        'post': 'timelog',
        })),
    url(r'^invite/', AddMemberViewset.as_view({
        'post': 'invite',
    }), name="invite"),
    url(r'^project-list/', ProjectsViewset.as_view({
        'get': 'list',
    }), name="projects"),
    url(r'^members/$', ProjectMembersViewset.as_view({
        'get': 'list',
        'post': 'none_members',
    }), name="members"),
    url(r'^members/logs/$', MemberLogsAPI.as_view({
        'get': 'logs',
    }), name="member_logs")
]