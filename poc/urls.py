from django.urls import path

from . import views

urlpatterns = [
    path('jobpost', views.job_post, name='job_post'),
    path('candidate', views.candidate_portal, name='candidate'),
]