from django.urls import path

from .views import *

urlpatterns = [
    path('companies/', CompanyListView.as_view(), name='api_companies'),
    path('company/<int:pk>/',CompanyDetailView.as_view(), name='api_company'),
    path('profiles/',ProfileListView.as_view(),name='api_profiles'),
    path('profile/<int:pk>/',ProfileDetailView.as_view(), name='api_profile'),
    path('rates/',RatesListView.as_view(),name="api_rates"),
    path('rate/<int:pk>/',RatesDetailView.as_view(),name="api_rate"),
    path('responses-to-companies/',ResponsesToCompanyListView.as_view(),name="api_res_to_companies"),
    path('response-to-company/<int:pk>/',ResponsesToCompanyDetailView.as_view(),name="api_res_to_company"),
    path('topics/', TopicListView.as_view(), name="api_topics"),
    path('topic-creation/', TopicCreateView.as_view(), name="api_create_topic"),
    path('boardthings/',BoardThingListView.as_view(),name='api_bt'),
    path('create-boardthings/',BoardThingCreateView.as_view(),name='api_create_bt'),
    path('tasks/',TaskListView.as_view(),name='api_tasks'),
    path('create-task/',TaskCreateView.as_view(),name='api_create_tasks'),
    path('g-or-b-jobs/',GorBListView.as_view(),name='api_g_or_b_jobs'),
    path('reports/',ReportListView.as_view(),name='api_reports'),
    path('report-<int:pk>/',ReportDetailView.as_view(),name='api_report'),
    path('responses-to-tasks/',ResponseToTaskListView.as_view(), name="api_responses_to_tasks"),
    path('response-to-task/<int:pk>/',ResponseToTaskDetailView.as_view(), name="api_response_to_task"),
]