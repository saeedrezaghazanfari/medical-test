from django.urls import path
from . import views


urlpatterns = [
    path('api/v1/get-user-data/', views.GetUserData.as_view()),
]