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
                    CompanyReadOnlyViewSet
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
    url(r'^timelog', LogViewSet.as_view({'get': 'current_log', 'post': 'timelog'}))
]