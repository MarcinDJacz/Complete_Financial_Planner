from django.urls import path
from planner.views import index, InmatesListView, InmatesDetailView

urlpatterns = [
    path("", index, name="index"),
    path("inmates/", InmatesListView.as_view(), name="inmates_list"),
    path("inmates/<int:pk>", InmatesDetailView.as_view(), name="inmates_detail"),
]

app_name = "planner"
