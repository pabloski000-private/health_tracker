from django.urls import path
from . import views

urlpatterns = [
    path("", views.calendar_view, name="calendar"),
    path("api/weights/", views.weights_json, name="weights_json"),
    path("api/weights/add/", views.add_weight, name="add_weight"),
    path("api/weights/series/", views.weights_series, name="weights_series"),
]