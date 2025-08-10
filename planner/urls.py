from django.urls import path
from planner.views import index


urlpatterns = [
    path("", index, name="index"),
]

app_name = "planner"
