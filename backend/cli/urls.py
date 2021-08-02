from django.conf.urls import url

from . import views

urlpatterns = [
    url(r"^execute", views.OrgCommandAPIView.as_view(), name="execute_command"),
    url(r"^change_db", views.DbCommandAPIView.as_view(), name="change_db"),
]
