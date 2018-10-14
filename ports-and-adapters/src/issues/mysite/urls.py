from django.urls import path

from issues import views

urlpatterns = [
    path('issues', views.list_issues, name='issues_list'),
    path('issues/<issue_id>', views.view_issue, name='issues_view'),
]
