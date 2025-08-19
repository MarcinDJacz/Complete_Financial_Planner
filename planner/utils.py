from .models import Savings, Debt, Portfolio
import plotly.graph_objs as go


def get_family_data(user):
    family = user.family
    savings = Savings.objects.filter(budget__family=family).order_by('date')
    debts = Debt.objects.filter(budget__family=family).order_by('date')
    portfolios = Portfolio.objects.filter(owner__family=family)

    investments = [
        instr
        for portfolio in portfolios
        for instr in portfolio.instrument_set.all()
    ]
    return savings, debts, investments


def get_all_dates(savings, debts, investments):
    return sorted(set(
        [s.date for s in savings] +
        [d.date for d in debts] +
        [i.date for i in investments]
    ))


def get_savings_cumulative(savings, dates):
    total = 0
    result = []
    for d in dates:
        total += sum(s.amount for s in savings if s.date == d)
        result.append(total)
    return result


def get_debts_cumulative(debts, dates):
    result = []
    for d in dates:
        total_debt = 0
        for debt in debts:
            if debt.date <= d:
                months_passed = ((d.year - debt.date.year) * 12
                                 + (d.month - debt.date.month))
                total_payment = (debt.rate or 0) * max(0, months_passed)
                total_debt += max(0, debt.amount - total_payment)
        result.append(total_debt)
    return result


def get_investments_cumulative(investments, dates):
    total = 0
    result = []
    for d in dates:
        total += sum(i.current_value for i in investments if i.date == d)
        result.append(total)
    return result


def build_finance_figure(dates, savings_cum, debts_cum, investments_cum):
    fig = go.Figure()
    fig.add_trace(go.Scatter(x=dates, y=savings_cum,
                             mode='lines', name='Savings'))
    fig.add_trace(go.Scatter(x=dates, y=debts_cum,
                             mode='lines', name='Debts'))
    fig.add_trace(go.Scatter(x=dates, y=investments_cum,
                             mode='lines', name='Investments'))
    fig.update_layout(title='Family Finance Overview')
    return fig


def get_family_graph(user):
    savings, debts, investments = get_family_data(user)
    dates = get_all_dates(savings, debts, investments)

    savings_cum = get_savings_cumulative(savings, dates)
    debts_cum = get_debts_cumulative(debts, dates)
    investments_cum = get_investments_cumulative(investments, dates)

    fig = build_finance_figure(dates, savings_cum, debts_cum, investments_cum)
    return fig.to_html(full_html=False)
