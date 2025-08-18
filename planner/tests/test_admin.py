from django.contrib.auth import get_user_model
from django.test import TestCase, Client
from django.urls import reverse


class AdminSiteTests(TestCase):
    def setUp(self):
        self.client = Client()
        self.admin_user = get_user_model().objects.create_superuser(
            username="admin",
            password="admin",
        )
        self.client.force_login(self.admin_user)
        self.casual_user = get_user_model().objects.create_user(
            first_name="XYZname",
            last_name="Kowalski",
            username="Thnos",
            email="marcin@gmail.com",
            password="<PASSWORD>",
        )

    def test_casual_user_name_listed(self):
        url = reverse("admin:planner_customuser_changelist")
        response = self.client.get(url)
        self.assertContains(response, self.casual_user.first_name)

    def test_casual_user_detail_name_listed(self):
        url = reverse("admin:planner_customuser_change", args=[self.casual_user.id])
        response = self.client.get(url)
        self.assertContains(response, self.casual_user.first_name)