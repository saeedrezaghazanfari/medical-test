from django.urls import path
from . import views


urlpatterns = [
    path('api/v1/get/patient/data/', views.GetPatientData.as_view()),
    path('api/v1/get/user/data/', views.GetUserData.as_view()),
    path('api/v1/create/sonography-center/', views.CreateSonographyCenter.as_view()),
    path('api/v1/create/lab/', views.CreateLab.as_view()),
    path('api/v1/create/lab-category/', views.CreateLabCategory.as_view()),
    path('api/v1/create/manager/', views.CreateManager.as_view()),
    # path('api/v1/user/password/', views.ChangePassword.as_view()),
]