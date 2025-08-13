from django.urls import path
from planner.views import (index,
                           InmatesListView,
                           InmatesDetailView,
                           UserSettingsView,
                           ContactMessageView,
                           OperationsListView,
                           OperationsCreateView,
                           OperationsDeleteView,
                           OperationsUpdateView)

urlpatterns = [
    path("", index, name="index"),
    path("inmates/", InmatesListView.as_view(), name="inmates_list"),
    path("inmates/<int:pk>", InmatesDetailView.as_view(), name="inmates_detail"),
    path("settings/", UserSettingsView.as_view(), name="user_settings"),
    path("contact/", ContactMessageView.as_view(), name="contact"),
    path("operations/", OperationsListView.as_view(), name="operations"),
    path("operations/create/", OperationsCreateView.as_view(), name="operations_create"),
    path("operations/<int:pk>/delete/", OperationsDeleteView.as_view(), name="operations_delete"),
    path("operations/<int:pk>/update/", OperationsUpdateView.as_view(), name="operations_update"),
]

app_name = "planner"
