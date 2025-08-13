from django.urls import path
from planner.views import index, InmatesListView, InmatesDetailView, UserSettingsView

urlpatterns = [
    path("", index, name="index"),
    path("inmates/", InmatesListView.as_view(), name="inmates_list"),
    path("inmates/<int:pk>", InmatesDetailView.as_view(), name="inmates_detail"),
    path("settings/", UserSettingsView.as_view(), name="user_settings"),
]

app_name = "planner"
