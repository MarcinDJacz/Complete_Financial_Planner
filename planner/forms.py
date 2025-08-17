from datetime import date

from django.contrib.auth import get_user_model
from django.contrib.auth.forms import UserCreationForm
from django import forms
from planner.models import CustomUser, Family, ContactMessage, Operation, Budget, Savings, Debt
from django.utils import timezone


class UserSettingsForm(forms.ModelForm):
    class Meta:
        model = CustomUser
        fields = ('email', 'first_name', 'last_name', 'family')


class FamilySettingsForm(forms.ModelForm):
    class Meta:
        model = Family
        fields = ('name',)


class ContactMessageForm(forms.ModelForm):
    class Meta:
        model = ContactMessage
        fields = ['name', 'email', 'subject', 'message']


class OperationCreateForm(forms.ModelForm):
    class Meta:
        model = Operation
        fields = ['budget', 'category', 'description', 'amount', 'date']

    def __init__(self, *args, **kwargs):
        user = kwargs.pop('user', None)
        super().__init__(*args, **kwargs)

        if user and hasattr(user, 'family'):
            budget = Budget.objects.filter(family=user.family).first()
            if budget:
                self.fields['budget'].initial = budget

        self.fields['date'].initial = timezone.now().date()


class CustomUserCreationForm(UserCreationForm):
    class Meta(UserCreationForm.Meta):
        model = CustomUser
        fields = ('username', 'first_name', 'last_name','email',)


class OperationSearchForm(forms.Form):
    description = forms.CharField(max_length=255,
                            required=False,
                            label="",
                            widget=forms.TextInput(attrs={'placeholder': 'Search by description'}))


class SavingsCreationForm(forms.ModelForm):
    class Meta:
        model = Savings
        fields = ('budget', 'category', 'amount', 'date')
        widgets = {
            'date': forms.DateInput(attrs={'type': 'date'}),
        }


class DebtCreationForm(forms.ModelForm):
    class Meta(UserCreationForm.Meta):
        model = Debt
        fields = ('budget', 'name', 'amount', 'date', 'due_date')
        widgets = {
            'date': forms.DateInput(attrs={'type': 'date'}),
            'due_date': forms.DateInput(attrs={'type': 'date'}),
        }
