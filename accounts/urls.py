from django.urls import path
from . import views

urlpatterns = [
    path('', views.authentication_view, name='authentication'),
    path('signup/', views.SignUpView.as_view(), name='signup'),
]