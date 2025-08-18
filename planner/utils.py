from .models import Savings, Debt, Portfolio
import plotly.graph_objs as go


def get_family_graph(user):
    family = user.family

    savings = Savings.objects.filter(budget__family=family).order_by('date')
    debts = Debt.objects.filter(budget__family=family).order_by('date')
    portfolios = Portfolio.objects.filter(owner__family=family)

    investments = []
    for portfolio in portfolios:
        for instr in portfolio.instrument_set.all():
            investments.append(instr)

    dates = sorted(set(
        [s.date for s in savings] +
        [d.date for d in debts] +
        [i.date for i in investments]
    ))

    savings_cum = []
    total_savings = 0
    for d in dates:
        total_savings += sum(s.amount for s in savings if s.date == d)
        savings_cum.append(total_savings)

    debts_cum = []
    for d in dates:
        total_debt = 0
        for debt in debts:
            if debt.date <= d:
                months_passed = max(0,
                                    (d.year - debt.date.year)
                                    * 12 + (d.month - debt.date.month))
                total_payment = (debt.rate or 0) * months_passed
                total_debt += max(0, debt.amount - total_payment)
        debts_cum.append(total_debt)

    investments_cum = []
    total_investments = 0
    for d in dates:
        total_investments += sum(i.current_value for
                                 i in investments if i.date == d)
        investments_cum.append(total_investments)

    fig = go.Figure()
    fig.add_trace(go.Scatter(x=dates,
                             y=savings_cum,
                             mode='lines',
                             name='Savings'))
    fig.add_trace(go.Scatter(x=dates,
                             y=debts_cum,
                             mode='lines',
                             name='Debts'))
    fig.add_trace(go.Scatter(x=dates,
                             y=investments_cum,
                             mode='lines',
                             name='Investments'))
    fig.update_layout(title='Family Finance Overview')

    return fig.to_html(full_html=False)
