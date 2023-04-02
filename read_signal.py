import time
import random

class TradeBot:
    def __init__(self, data_source, broker):
        self.data_source = data_source
        self.broker = broker
        self.portfolio = {}  # Dictionary to keep track of our holdings for each symbol
        self.rules = [  # List of rules that define when to buy or sell a symbol
            {"symbol": "AAPL", "buy_if": "price_below", "sell_if": "price_above", "price": 120},
            {"symbol": "GOOG", "buy_if": "price_below", "sell_if": "price_above", "price": 2000},
            {"symbol": "MSFT", "buy_if": "price_below", "sell_if": "price_above", "price": 250},
        ]

    def read_trade_signals(self):
        signals = self.data_source.get_trade_signals()  # Get the latest trade signals from the data source
        return signals

    def execute_trade(self, signal):
        symbol = signal["symbol"]
        action = signal["action"]
        quantity = signal["quantity"]
        if action == "buy":
            self.broker.buy(symbol, quantity)  # Buy the specified symbol and quantity
            self.portfolio[symbol] = quantity  # Add the symbol and quantity to our portfolio
        elif action == "sell":
            self.broker.sell(symbol, quantity)  # Sell the specified symbol and quantity
            self.portfolio[symbol] -= quantity  # Subtract the quantity from our portfolio

    def run(self):
        while True:
            signals = self.read_trade_signals()
            for signal in signals:
                self.execute_trade(signal)
            for symbol, holdings in self.portfolio.items():
                current_price = self.data_source.get_price(symbol)
                for rule in self.rules:
                    if rule["symbol"] == symbol:
                        if rule["buy_if"] == "price_below" and current_price < rule["price"]:
                            buy_quantity = min(holdings, int(self.broker.get_buying_power() / current_price))
                            if buy_quantity > 0:
                                self.broker.buy(symbol, buy_quantity)
                                self.portfolio[symbol] += buy_quantity
                        elif rule["sell_if"] == "price_above" and current_price > rule["price"]:
                            sell_quantity = holdings
                            if sell_quantity > 0:
                                self.broker.sell(symbol, sell_quantity)
                                self.portfolio[symbol] -= sell_quantity
            time.sleep(random.randint(5, 15))  # Wait for a random number of seconds between 5 and 15 before checking for new signals again
