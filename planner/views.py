from django.contrib.auth.forms import UserCreationForm
from django.shortcuts import render
from django.urls import reverse_lazy
from django.db.models import Sum
from .models import CustomUser, Operation, Savings, Debt, Portfolio, Family, ContactMessage
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views import generic
from .forms import UserSettingsForm, DebtCreationForm, FamilySettingsForm, SavingsCreationForm, OperationSearchForm, ContactMessageForm, OperationCreateForm, CustomUserCreationForm
from .utils import get_family_graph


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
    num_portfolio = portfolios.count()
    total_value = sum(p.current_value for p in portfolios)
    messages_num = ContactMessage.objects.filter(is_read=False).count()
    context = {
        "family_name" : request.user.family.name,
        "num_inmates": num_inmates,
        "income_sum": income_sum,
        "expense_sum": expense_sum,
        "summary_savings": summary_savings,
        "summary_debts": summary_debts,
        "num_visit": num_visit + 1,
        "surplus_deficit": (income_sum - expense_sum),
        "portfolios": portfolios,
        "summary_investments": round(total_value,2),
        "sum_saving_sum_debts": (summary_savings - summary_debts),
        "messages_num": messages_num,
        "num_portfolio": num_portfolio,
    }
    context['graph_html'] = get_family_graph(request.user)
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
        context = super(OperationsListView, self).get_context_data(**kwargs)
        description = self.request.GET.get("description", "")
        context["search_form"] = OperationSearchForm(initial={"description": description})
        per_page = self.request.GET.get('per_page')
        context['per_page_value'] = int(per_page) if per_page and per_page.isdigit() else 10
        return context

    def get_queryset(self):
        queryset = Operation.objects.all()
        form = OperationSearchForm(self.request.GET)
        if form.is_valid() and form.cleaned_data.get("description"):
            queryset = queryset.filter(description__icontains=form.cleaned_data["description"])
        return queryset

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
    template_name = "planner/user_create_form.html"


class DashboardView(LoginRequiredMixin, generic.TemplateView):
    template_name = "planner/dashboard.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        context['graph_html'] = get_family_graph(self.request.user)
        return context


class FamilyUpdateView(LoginRequiredMixin, generic.UpdateView):
    model = Family
    form_class = FamilySettingsForm

    def get_object(self, queryset=None):
        return self.request.user.family

    success_url = reverse_lazy('planner:inmates_list')
    template_name = "planner/family_update.html"


class MessagesListView(LoginRequiredMixin, generic.ListView):
    model = ContactMessage
    template_name = "planner/messages_list.html"
    context_object_name = "messages"

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


class MessageDetailView(LoginRequiredMixin, generic.DetailView):
    model = ContactMessage
    template_name = "planner/message_detail.html"

    def get_object(self, queryset=None):
        obj = super().get_object(queryset)
        if not obj.is_read:
            obj.is_read = True
            obj.save(update_fields=["is_read"])
        return obj


class MessagesDeleteView(LoginRequiredMixin, generic.DeleteView):
    model = ContactMessage
    fields = '__all__'
    template_name = "planner/message_format_confirm_delete.html"
    success_url = reverse_lazy('planner:messages_list')


class SavingsDebtsListView(LoginRequiredMixin, generic.ListView):
    model = Savings
    template_name = "planner/savings_and_debts.html"
    context_object_name = "savings_and_debts"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["savings"] = Savings.objects.all()
        context["debts"] = Debt.objects.all()
        return context


class SavingsCreateView(LoginRequiredMixin, generic.CreateView):
    model = Savings
    form_class = SavingsCreationForm
    success_url = reverse_lazy('planner:savings_and_debts')
    template_name = "planner/savings_create_form.html"


class SavingsUpdateView(LoginRequiredMixin, generic.UpdateView):
    model = Savings
    fields = '__all__'
    success_url = reverse_lazy('planner:savings_and_debts')
    template_name = "planner/savings_update_form.html"


class SavingsDeleteView(LoginRequiredMixin, generic.DeleteView):
    model = Savings
    fields = '__all__'
    template_name = "planner/savings_format_confirm_delete.html"
    success_url = reverse_lazy('planner:savings_and_debts')


class DebtsCreateView(LoginRequiredMixin, generic.CreateView):
    model = Debt
    form_class = DebtCreationForm
    success_url = reverse_lazy('planner:savings_and_debts')
    template_name = "planner/debts_create_form.html"

class DebtsDeleteView(LoginRequiredMixin, generic.DeleteView):
    model = Debt
    fields = '__all__'
    template_name = "planner/debts_format_confirm_delete.html"
    success_url = reverse_lazy('planner:savings_and_debts')


class DebtsUpdateView(LoginRequiredMixin, generic.UpdateView):
    model = Debt
    fields = '__all__'
    success_url = reverse_lazy('planner:savings_and_debts')
    template_name = "planner/debt_update_form.html"