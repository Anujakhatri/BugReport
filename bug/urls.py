from django.urls import path

from . import views

urlpatterns = [
    # Frontend template view
    path('', views.index, name='index'),

    # API views
    path('api/reports/', views.bug_list_create_view, name='bug_list_create'),
    path('api/reports/<int:pk>/', views.bug_detail_view, name='bug_detail'),
    path('api/reports/<int:pk>/ai-review/', views.bug_ai_review, name='bug_ai_review'),
]