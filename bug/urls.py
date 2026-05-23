from django.urls import path


from .views import bug_report_view, bug_report_post, bug_report_detail

urlpatterns = [
    #function based views
    path('bug-reports/', bug_report_view, name='bug_report_view' ),
    path('bug-report/create/', bug_report_post, name='bug_report_post' ),
    path('bug-report/<int:pk>/', bug_report_detail, name='bug_report_detail'),
]