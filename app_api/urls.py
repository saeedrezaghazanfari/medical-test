from django.urls import path
from . import views


urlpatterns = [
    path('api/v1/patient/results/sono/', views.GetPatientSono.as_view()),
    path('api/v1/patient/results/lab/', views.GetPatientLab.as_view()),
    path('api/v1/patient/exists/', views.IsPatient.as_view()),
    path('api/v1/get/user/data/', views.GetUserData.as_view()),
    path('api/v1/create/sonography-center/', views.CreateSonographyCenter.as_view()),
    path('api/v1/create/lab/', views.CreateLab.as_view()),
    path('api/v1/create/lab-category/', views.CreateLabCategory.as_view()),
    path('api/v1/create/lab-subcategory/', views.CreateLabSUBCategory.as_view()),
    path('api/v1/create/manager/', views.CreateManager.as_view()),
    path('api/v1/create/doctor/', views.CreateDoctor.as_view()),
    path('api/v1/create/patient/', views.CreatePatient.as_view()),
    path('api/v1/create/patient/lab/', views.PatientLab.as_view()),
    path('api/v1/create/patient/sonography/', views.PatientSonography.as_view()),
    # path('api/v1/user/password/', views.ChangePassword.as_view()),
]