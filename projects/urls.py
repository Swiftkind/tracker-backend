from django.conf.urls import url

from .views import (
                    TimeLogTemplateView,
                    AdminTemplateView,
                )
urlpatterns = [
    url(r'^timelog', TimeLogTemplateView.as_view(), name='timelog'),
    url(r'^timesheet', AdminTemplateView.as_view(), name='timesheet')
]