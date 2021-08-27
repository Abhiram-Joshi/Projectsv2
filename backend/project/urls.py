from django.conf.urls import url

from . import views

urlpatterns = [
    url(r"get_data", views.ProjectDataAPIView.as_view(), name="project_data"),
    url(r"issues", views.ProjectIssuesAPIView.as_view(), name="project_issues"),
    url(r"contributors", views.ProjectContributorsAPIView.as_view(), name="project_contributors"),
    url(r"languages", views.ProjectLanguagesAPIView.as_view(), name="project_languages"),
    url(r"pull_requests", views.ProjectPullRequestsAPIView.as_view(), name="project_pull_requests"),
    url(r"get_year", views.ProjectYearAPIView.as_view(), name="project_year"),
]
