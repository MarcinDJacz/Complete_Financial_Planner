from django.core.management.base import BaseCommand
from datetime import date
import requests
from planner.models import CurrencyRate, StockPrice, Instrument
import yfinance as yf


class Command(BaseCommand):
    help = 'Fetches currency exchange rates and stock prices, and saves them to the database'

    BASE_CURRENCY = 'PLN'

    def handle(self, *args, **options):
        self.stdout.write("Fetching currency exchange rates...")
        self.update_currency_rates()

        self.stdout.write("Fetching stock prices...")
        self.update_stock_prices()

        self.stdout.write("Update completed.")

    def update_currency_rates(self):
        # List of currencies to fetch
        currencies = ['USD', 'EUR', 'GBP']

        # Fetch rates relative to BASE_CURRENCY (PLN)
        for curr in currencies:
            if curr == self.BASE_CURRENCY:
                rate = 1.0
            else:
                url = f"https://api.exchangerate.host/latest?base={self.BASE_CURRENCY}&symbols={curr}"
                resp = requests.get(url)
                data = resp.json()
                rate = data['rates'].get(curr)

            if rate:
                obj, created = CurrencyRate.objects.update_or_create(
                    currency_code=curr,
                    date_fetched=date.today(),
                    defaults={'rate_to_base': rate}
                )
                action = "Created" if created else "Updated"
                self.stdout.write(f"{action} exchange rate {curr}: {rate}")

    def update_stock_prices(self):
        # Get unique stock symbols from Instruments
        symbols = Instrument.objects.values_list('symbol', flat=True).distinct()

        for symbol in symbols:
            # Simple example using yfinance (can be adjusted)
            try:
                stock = yf.Ticker(symbol)
                hist = stock.history(period='1d')
                if not hist.empty:
                    price = hist['Close'][0]
                    obj, created = StockPrice.objects.update_or_create(
                        symbol=symbol,
                        date_fetched=date.today(),
                        defaults={'price': price}
                    )
                    action = "Created" if created else "Updated"
                    self.stdout.write(f"{action} price {symbol}: {price}")
                else:
                    self.stdout.write(f"No data for {symbol}")
            except Exception as e:
                self.stdout.write(f"Error while fetching price for {symbol}: {str(e)}")
