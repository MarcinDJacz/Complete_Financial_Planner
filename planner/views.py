from django.shortcuts import render
from django.urls import reverse_lazy
from django.db.models import Sum
from .models import CustomUser, Operation
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views import generic
from .forms import UserSettingsForm, ContactMessageForm


@login_required
def index(request):
    num_inmates = CustomUser.objects.all().count()
    summary_savings = 0  # on start
    summary_debts = 0
    income_sum = Operation.objects.filter(category__type='INCOME').aggregate(total=Sum('amount'))['total'] or 0

    expense_sum = Operation.objects.filter(category__type='EXPENSE').aggregate(total=Sum('amount'))['total'] or 0


    summary_investments = 0  # add to model budget total_investments
    num_visit = request.session.get('num_visit', 0)
    request.session['num_visit'] = num_visit + 1

    context = {
        "num_inmates": num_inmates,
        "income_sum": income_sum,
        "expense_sum": expense_sum,
        "summary_savings": summary_savings,
        "summary_debts": summary_debts,
        "summary_investments": summary_investments,
        "num_visit": num_visit + 1,
        "surplus_deficit": (income_sum - expense_sum)
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