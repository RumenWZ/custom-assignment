from django.urls import path

from CustomAssignment.api.views import apiStats

urlpatterns = (
    path('stats/', apiStats, name='stats'),
)