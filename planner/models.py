from django.db import models
from django.contrib.auth.models import AbstractUser
from django.conf import settings
from django.urls import reverse


class Family(models.Model):
    name = models.CharField(max_length=100, unique=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name


class CustomUser(AbstractUser):
    date_of_birth = models.DateField(null=True, blank=True)
    family = models.ForeignKey(
        'Family',
        on_delete=models.CASCADE,
        related_name='members',
        null=True,
        blank=True
    )

    def __str__(self):
        return self.username

    def get_absolute_url(self):
        return reverse("planner:inmates_detail", args=[str(self.id)])


class Category(models.Model):
    name = models.CharField(max_length=100)
    CATEGORY_TYPES = [
        ('INCOME', 'Income'),
        ('EXPENSE', 'Expense'),
    ]
    type = models.CharField(max_length=10, choices=CATEGORY_TYPES)

    def __str__(self):
        return f"{self.name} ({self.type})"


class Budget(models.Model):
    family = models.OneToOneField(Family, on_delete=models.CASCADE,
                                  related_name='budget',
                                  null=True,
                                  blank=True)
    name = models.CharField(max_length=100)
    total_amount = models.DecimalField(max_digits=12, decimal_places=2)
    start_date = models.DateField()
    end_date = models.DateField()

    def __str__(self):
        return f"{self.name} - {self.family}"


class Operation(models.Model):
    budget = models.ForeignKey(Budget, on_delete=models.CASCADE,
                               related_name='operations')
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    created_by = models.ForeignKey(settings.AUTH_USER_MODEL,
                                   on_delete=models.SET_NULL, null=True)
    description = models.TextField(blank=True)
    amount = models.DecimalField(max_digits=12, decimal_places=2)
    date = models.DateField()

    def __str__(self):
        return f"{self.category} - {self.amount}"


class Debt(models.Model):
    budget = models.ForeignKey(Budget, on_delete=models.CASCADE)
    name = models.CharField(max_length=100)
    amount = models.DecimalField(max_digits=12, decimal_places=2)
    date = models.DateField(null=True, blank=True)
    rate = models.DecimalField(max_digits=12, decimal_places=2, default=0)
    due_date = models.DateField()

    def __str__(self):
        return f"{self.name} - {self.amount}"


class SavingCategory(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name


class Savings(models.Model):
    budget = models.ForeignKey(Budget, on_delete=models.CASCADE)
    category = models.ForeignKey(SavingCategory,
                                 on_delete=models.SET_NULL, null=True)
    amount = models.DecimalField(max_digits=12, decimal_places=2)
    date = models.DateField(null=True, blank=True)

    def __str__(self):
        return f"{self.category} - {self.amount}"


class Portfolio(models.Model):
    owner = models.ForeignKey(settings.AUTH_USER_MODEL,
                              on_delete=models.CASCADE)
    name = models.CharField(max_length=100)

    def __str__(self):
        return f"{self.name} ({self.owner})"

    @property
    def current_value(self):
        return round(sum(instr.current_value for instr in self.instrument_set.all()), 2)


class Instrument(models.Model):
    portfolio = models.ForeignKey(Portfolio, on_delete=models.CASCADE)
    symbol = models.CharField(max_length=10, db_index=True)
    name = models.CharField(max_length=100)
    quantity = models.DecimalField(max_digits=12, decimal_places=4)
    date = models.DateField(null=True, blank=True)

    def __str__(self):
        return f"{self.symbol} - {self.quantity}"

    @property
    def current_value(self):
        latest_price = StockPrice.get_latest_price(self.symbol)
        if latest_price:
            return round(self.quantity * latest_price.price, 2)
        return 0


class CurrencyRate(models.Model):
    currency_code = models.CharField(max_length=3, db_index=True)
    rate_to_base = models.DecimalField(max_digits=12, decimal_places=6)
    date_fetched = models.DateField()

    class Meta:
        unique_together = ('currency_code', 'date_fetched')

    def __str__(self):
        return (f"{self.currency_code} - {self.rate_to_base} "
                f"({self.date_fetched})")

    @classmethod
    def get_latest_rate(cls, currency_code):
        return (cls.objects.filter(currency_code=currency_code)
                .order_by('-date_fetched').first())


class StockPrice(models.Model):
    symbol = models.CharField(max_length=10, db_index=True)
    price = models.DecimalField(max_digits=12, decimal_places=4)
    date_fetched = models.DateField()

    class Meta:
        unique_together = ('symbol', 'date_fetched')

    def __str__(self):
        return f"{self.symbol} - {self.price} ({self.date_fetched})"

    @classmethod
    def get_latest_price(cls, symbol):
        return (cls.objects.filter(symbol=symbol)
                .order_by('-date_fetched').first())


class ContactMessage(models.Model):
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='contact_messages'
    )
    name = models.CharField(max_length=100)
    email = models.EmailField()
    subject = models.CharField(max_length=150)
    message = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    is_read = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.subject} from {self.name}"
