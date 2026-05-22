from django.urls import path
from .views import BugReportAPI

urlpatterns = [
    path('bug-reports/', BugReportAPI.as_view()),
]