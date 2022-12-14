from django.urls import path
from . import views


urlpatterns = [
    path('api/v1/get-patient-data/', views.GetPatientData.as_view()),
]