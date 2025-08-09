from django.contrib import admin
from .models import Category, Family, Budget, Operation, Debt, SavingCategory, Savings, Portfolio, Instrument, CurrencyRate, StockPrice


admin.site.register(Category)
admin.site.register(Budget)
admin.site.register(Operation)
admin.site.register(Debt)
admin.site.register(SavingCategory)
admin.site.register(Savings)
admin.site.register(Portfolio)
admin.site.register(Instrument)
admin.site.register(CurrencyRate)
admin.site.register(StockPrice)
admin.site.register(Family)
