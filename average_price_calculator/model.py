from enum import Enum
import re

class Operation(Enum):
    C = 'COMPRA'
    V = 'VENDA'

class Type(Enum):
    VISTA = 'VISTA'
    FRACIONARIO = 'FRACIONARIO'

class Trade:

    def __init__(self, text: list, no_standard_ticker_names = {}) -> None:
        values = re.split(r'\s+', text)
        self.operation = None
        self.type = None
        self.ticker = None
        self.quantity = None
        self.unitary_price = None
        numbers = []
        for value in values:
            v = value.strip()
            n = self.format_number(v)
            if v in Operation.__members__:
                self.operation = Operation[v]
            elif v in Type.__members__:
                self.type = Type[v]
            elif v in no_standard_ticker_names.keys():
                self.ticker = no_standard_ticker_names[v]
            elif re.fullmatch(r'[A-Z]{4}\d{1,2}F?', v):
                self.ticker = v
            elif type(n) == int:
                self.quantity = n
            elif type(n) == float:
                numbers.append(n)
        numbers.sort()
        if len(numbers) > 0:
            self.unitary_price = numbers[0]


    def format_number(self, text):
        try:
            sanitized = text.replace(',', '.').strip()
            return float(sanitized) if '.' in sanitized else int(sanitized)
        except ValueError:
            return None

    @property   
    def total(self):
        return self.quantity * self.unitary_price
    
    def __str__(self) -> str:
        return f'{self.operation.value if self.operation else None} | {self.type.value if self.type else None} | {self.ticker} | {self.quantity} | {self.unitary_price}'
    
class Stock:

    def __init__(self, ticker) -> None:
        self.ticker = ticker 
        self.trades = []

    def addTrade(self, trade: Trade):
        self.trades.append(trade)

    @property
    def average_price(self):
        total_value_purchase = sum([ trade.total for trade in self.trades if trade.operation == Operation.C ])
        qtd_purchase = sum([ trade.quantity for trade in self.trades if trade.operation == Operation.C ])
        average_purchase = total_value_purchase / qtd_purchase
        qtd_sale = sum([ trade.quantity for trade in self.trades if trade.operation == Operation.V ])
        total_value_sale = average_purchase * qtd_sale
        total_value = total_value_purchase - total_value_sale
        qtd_total = qtd_purchase - qtd_sale
        return total_value / qtd_total if qtd_total > 0 else .0

    def __eq__(self, other: object) -> bool:
        if type(other) != Stock:
            return False
        return self.ticker == other.ticker
    
    def __str__(self) -> str:
        return f'{self.ticker}: {[str(trade) for trade in self.trades]}'
