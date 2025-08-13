from datetime import date

from django.contrib.auth import get_user_model
from django.contrib.auth.forms import UserCreationForm
from django import forms
from planner.models import CustomUser, ContactMessage, Operation, Budget
from django.utils import timezone


class UserSettingsForm(forms.ModelForm):
    class Meta:
        model = CustomUser
        fields = ('email', 'first_name', 'last_name', 'family')


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