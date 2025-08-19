import requests
import time
import yfinance as yf
from datetime import date
from django.conf import settings
from django.core.management.base import BaseCommand

from planner.models import CurrencyRate, StockPrice, Instrument


class Command(BaseCommand):
    help = 'Fetches currency exchange rates and stock prices, and saves them to the database'

    BASE_CURRENCY = 'EUR'

    def handle(self, *args, **options):
        self.stdout.write("Fetching currency exchange rates...")
        self.update_currency_rates()

        self.stdout.write("Fetching stock prices...")
        self.update_stock_prices()

        self.stdout.write("Update completed.")

    def update_currency_rates(self):
        # List of currencies to fetch
        api_key = getattr(settings, "EXCHANGERATESAPI_KEY", None)
        if not api_key:
            self.stderr.write("No EXCHANGERATESAPI_KEY in settings.py lub w zmiennych środowiskowych")
            return
        currencies = ['USD', 'PLN', 'GBP']
        for curr in currencies:
            if curr == self.BASE_CURRENCY:
                rate = 1.0
            else:
                url = f"https://api.exchangeratesapi.io/v1/latest"
                try:
                    resp = requests.get(
                        url,
                        params={"base": self.BASE_CURRENCY,
                                "symbols": curr,
                                "access_key": api_key},
                        timeout=10
                    )
                    resp.raise_for_status()
                    data = resp.json()

                    rate = data.get("rates", {}).get(curr)
                    if rate is None:
                        self.stderr.write(f"No rate for {curr} in API response: {data}")
                        continue
                except (requests.exceptions.RequestException, ValueError) as e:

                    self.stderr.write(f"Error fetching rate for {curr}: {e}")
                    continue

            obj, created = CurrencyRate.objects.update_or_create(
                currency_code=curr,
                date_fetched=date.today(),
                defaults={"rate_to_base": rate}
            )
            action = "Created" if created else "Updated"
            self.stdout.write(f"{action} exchange rate {curr}: {rate}")
            time.sleep(1)

    def update_stock_prices(self):
        # Get unique stock symbols from Instruments
        symbols = Instrument.objects.exclude(symbol="$").values_list('symbol', flat=True).distinct()
        for symbol in symbols:
            try:
                symbol+=".WA"
                stock = yf.Ticker(symbol)
                hist = stock.history(period='1d')
                if not hist.empty:
                    price = hist['Close'].iloc[0]
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
