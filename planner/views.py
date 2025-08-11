from django.shortcuts import render
from .models import CustomUser, Budget
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views import generic


@login_required
def index(request):
    num_inmates = CustomUser.objects.all().count()
    summary_savings = 0 # on start
    summary_debts = 0 #  Budget.total_debt.all().count() # add to model budget total_debt
    summary_investments = 0 # add to model budget total_investments
    num_visit = request.session.get('num_visit', 0)
    request.session['num_visit'] = num_visit + 1
    context = {
        "num_inmates": num_inmates,
        "summary_savings": summary_savings,
        "summary_debts": summary_debts,
        "summary_investments": summary_investments,
        "num_visit": num_visit + 1,
    }
    return render(request,'planner/index.html', context)


class InmatesListView(LoginRequiredMixin, generic.ListView):
    model = CustomUser
    template_name = "planner/inmates_list.html"
    context_object_name = "inmates"
