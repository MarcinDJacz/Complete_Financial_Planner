from django.urls import path
from planner.views import index, InmatesListView, InmatesDetailView, UserSettingsView, ContactMessageView

urlpatterns = [
    path("", index, name="index"),
    path("inmates/", InmatesListView.as_view(), name="inmates_list"),
    path("inmates/<int:pk>", InmatesDetailView.as_view(), name="inmates_detail"),
    path("settings/", UserSettingsView.as_view(), name="user_settings"),
    path("contact/", ContactMessageView.as_view(), name="contact"),
]

app_name = "planner"
