from django.urls import path
from django.shortcuts import redirect
from . import views

urlpatterns = [
    path("rest/v1/calendar/init/", views.GoogleCalendarInitView, name="auth"),
    path('', lambda req: redirect('auth')),
    path("rest/v1/calendar/redirect/", views.GoogleCalendarRedirectView, name="redir")
]
