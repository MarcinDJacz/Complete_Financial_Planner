from django.contrib.auth.forms import UserCreationForm
from django.shortcuts import render
from django.urls import reverse_lazy
from django.db.models import Sum
from .models import CustomUser, Operation, Savings, Debt, Portfolio
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views import generic
from .forms import UserSettingsForm, ContactMessageForm, OperationCreateForm, CustomUserCreationForm


@login_required
def index(request):
    num_inmates = CustomUser.objects.all().count()
    summary_savings = Savings.objects.aggregate(total=Sum('amount'))['total'] or 0
    summary_debts = Debt.objects.aggregate(total=Sum('amount'))['total'] or 0
    income_sum = Operation.objects.filter(category__type='INCOME').aggregate(total=Sum('amount'))['total'] or 0

    expense_sum = Operation.objects.filter(category__type='EXPENSE').aggregate(total=Sum('amount'))['total'] or 0

    num_visit = request.session.get('num_visit', 0)
    request.session['num_visit'] = num_visit + 1

    portfolios = Portfolio.objects.all()
    total_value = sum(p.current_value for p in portfolios)

    context = {
        "num_inmates": num_inmates,
        "income_sum": income_sum,
        "expense_sum": expense_sum,
        "summary_savings": summary_savings,
        "summary_debts": summary_debts,
        "num_visit": num_visit + 1,
        "surplus_deficit": (income_sum - expense_sum),
        "portfolios": portfolios,
        "summary_investments": total_value,
    }
    return render(request, 'planner/index.html', context)


class InmatesListView(LoginRequiredMixin, generic.ListView):
    model = CustomUser
    template_name = "planner/inmates_list.html"
    context_object_name = "inmates"


class InmatesDetailView(LoginRequiredMixin, generic.DetailView):
    model = CustomUser
    template_name = "planner/inmates_detail.html"


class UserSettingsView(LoginRequiredMixin, generic.UpdateView):
    model = CustomUser
    form_class = UserSettingsForm

    def get_object(self, queryset=None):
        return self.request.user


class ContactMessageView(generic.FormView):
    template_name = 'planner/contact.html'
    form_class = ContactMessageForm
    success_url = reverse_lazy('planner:index')

    def form_valid(self, form):
        if self.request.user.is_authenticated:
            form.instance.user = self.request.user
        form.save()
        return super().form_valid(form)

class OperationsListView(LoginRequiredMixin, generic.ListView):
    model = Operation
    template_name = "planner/operations_list.html"
    context_object_name = "operations"

    def get_paginate_by(self, queryset):
        per_page = self.request.GET.get('per_page')
        if per_page and per_page.isdigit():
            return int(per_page)
        return 10

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        per_page = self.request.GET.get('per_page')
        context['per_page_value'] = int(per_page) if per_page and per_page.isdigit() else 10
        return context

class OperationsCreateView(LoginRequiredMixin, generic.CreateView):
    model = Operation
    form_class = OperationCreateForm
    success_url = reverse_lazy('planner:operations')

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs['user'] = self.request.user
        return kwargs


class OperationsDeleteView(LoginRequiredMixin, generic.DeleteView):
    model = Operation
    fields = '__all__'
    template_name = "planner/operations_format_confirm_delete.html"
    success_url = reverse_lazy('planner:operations')


class OperationsUpdateView(LoginRequiredMixin, generic.UpdateView):
    model = Operation
    fields = '__all__'
    success_url = reverse_lazy('planner:operations')
    template_name = "planner/operations_update_form.html"


class InmateCreateView(generic.CreateView):
    model = CustomUser
    form_class = CustomUserCreationForm
    success_url = reverse_lazy('planner:index')