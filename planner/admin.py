from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import (Category,
                     CustomUser,
                     Family,
                     Budget,
                     Operation,
                     Debt,
                     SavingCategory,
                     Savings,
                     Portfolio,
                     Instrument,
                     CurrencyRate,
                     StockPrice,
                     ContactMessage)

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
admin.site.register(ContactMessage)


@admin.register(CustomUser)
class CustomUserAdmin(UserAdmin):
    pass
