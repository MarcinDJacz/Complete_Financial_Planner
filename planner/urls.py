from django.urls import path
from planner.views import index, InmatesListView

urlpatterns = [
    path("", index, name="index"),
    path("inmates/", InmatesListView.as_view(), name="inmates_list"),
]

app_name = "planner"
