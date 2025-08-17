from django.urls import path
from planner.views import (index,
                           InmatesListView,
                           InmatesDetailView,
                           UserSettingsView,
                           ContactMessageView,
                           OperationsListView,
                           OperationsCreateView,
                           OperationsDeleteView,
                           OperationsUpdateView,
                           InmateCreateView,
                           DashboardView,
                           FamilyUpdateView,
                           MessagesListView,
                           MessageDetailView)

urlpatterns = [
    path("", index, name="index"),
    path("inmates/", InmatesListView.as_view(), name="inmates_list"),
    path("inmates/<int:pk>", InmatesDetailView.as_view(), name="inmates_detail"),
    path("settings/", UserSettingsView.as_view(), name="user_settings"),
    path("contact/", ContactMessageView.as_view(), name="contact"),
    path("messages/", MessagesListView.as_view(), name="messages_list"),
    path("messages/<int:pk>", MessageDetailView.as_view(), name="message_detail"),
    path("operations/", OperationsListView.as_view(), name="operations"),
    path("operations/create/", OperationsCreateView.as_view(), name="operations_create"),
    path("operations/<int:pk>/delete/", OperationsDeleteView.as_view(), name="operations_delete"),
    path("operations/<int:pk>/update/", OperationsUpdateView.as_view(), name="operations_update"),
    path("inmates/create/", InmateCreateView.as_view(), name="inmate-create"),
    path("dashboard/", DashboardView.as_view(), name="dashboard"),
    path("family/<int:pk>/update/", FamilyUpdateView.as_view(), name="family_update"),
    ]

app_name = "planner"
