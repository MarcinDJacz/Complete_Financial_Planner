from django.test import TestCase
from planner.models import CustomUser, Family, Budget, Category
from planner.forms import OperationCreateForm
from django.utils import timezone

class FormsTests(TestCase):
    def setUp(self):
        self.user = CustomUser.objects.create_user(username="testuser", password="pass")
        self.family = Family.objects.create(name="Test Family")
        self.user.family = self.family
        self.user.save()
        self.budget = Budget.objects.create(
            name="Test Budget",
            family=self.family,
            total_amount=1000,
            start_date="2025-08-11",
            end_date="2025-08-11"
        )
        self.category = Category.objects.create(name="Food")

    def test_operation_creation_form(self):
        form_data = {
            "budget": self.budget.id,
            "category": self.category.id,
            "description": "opis",
            "amount": "123",
            "date": timezone.now().date(),
            "created_by": self.user,
        }
        form = OperationCreateForm(data=form_data, user=self.user)
        print(form.errors)
        self.assertTrue(form.is_valid())
        self.assertEqual(form.cleaned_data['date'], form_data['date'])
