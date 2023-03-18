from django.urls import path
from . import views
urlpatterns = [
    path("", views.Show_Air_Chart_View, name="charts"),
]
