from enum import Enum
import re

class Operation(Enum):
    C = 'COMPRA'
    V = 'VENDA'

class Type(Enum):
    VISTA = 'VISTA'
    FRACIONARIO = 'FRACIONARIO'

class Trade:

    def __init__(self, text: list) -> None:
        values = re.split(r'\s+', text)
        self.operation = None
        self.type = None
        self.ticker = None
        self._quantity = None
        self.unitary_price = None
        numbers = []
        for value in values:
            v = value.strip()
            n = self.format_number(v)
            if v in Operation.__members__:
                self.operation = Operation[v]
            elif v in Type.__members__:
                self.type = Type[v]
            elif re.fullmatch(r'[A-Z]{4}\d{1,2}F?', v):
                self.ticker = v
            elif type(n) == int:
                self._quantity = n
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
    
    @property
    def quantity(self):
        signal = 1 if self.operation == Operation.C else -1
        return self._quantity * signal
    
    @quantity.setter
    def quantity(self, quantity):
        self._quantity = quantity

    def __str__(self) -> str:
        return f'{self.operation.value if self.operation else None} | {self.type.value if self.type else None} | {self.ticker} | {self.quantity} | {self.unitary_price}'
    
class Stock:

    def __init__(self, ticker) -> None:
        self.ticker = ticker 
        self.trades = []

    def addTrade(self, trade: Trade):
        self.trades.append(trade)

    def average_price(self):
        total_value = sum([ trade.total for trade in self.trades ])
        qtd = sum([ trade.quantity for trade in self.trades ])
        return total_value / qtd if qtd > 0 else .0

    def __eq__(self, other: object) -> bool:
        if type(other) != Stock:
            return False
        return self.ticker == other.ticker
    
    def __str__(self) -> str:
        return f'{self.ticker}: {[str(trade) for trade in self.trades]}'
