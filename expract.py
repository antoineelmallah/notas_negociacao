import pdfquery
import os
from enum import Enum
import re


def get_box_positions_between_texts(pdf: pdfquery.PDFQuery, common_value_field):
    return [(0.0, float(item.attrib['y0']), 600.0, float(item.attrib['y1'])) for item in pdf.pq(f'LTTextLineHorizontal:contains("{ common_value_field }")')]


def read_table(path):
    pdf = pdfquery.PDFQuery(path)

    pdf.load()
 
    limits = get_box_positions_between_texts(pdf, 'BOVESPA')

    return [ pdf.pq('LTTextLineHorizontal:overlaps_bbox("%s, %s, %s, %s")' % line).text() for line in limits]


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
            
    def getTotal(self):
        
        return self.quantity * self.unitary_price

    def __str__(self) -> str:
        return f'{self.operation.value if self.operation else None} | {self.type.value if self.type else None} | {self.ticker} | {self.quantity} | {self.unitary_price}'
    
class Stock:

    def __init__(self, ticker) -> None:
        self.ticker = ticker 
        self.trades = []

    def addTrade(self, trade: Trade):
        self.trades.append(trade)

    def __eq__(self, __value: object) -> bool:
        if type(__value) != Stock:
            return False
        return self.ticker == __value.ticker
    
    def __str__(self) -> str:
        return f'{self.ticker}: {[str(trade) for trade in self.trades]}'

result = []

for year in ('2019', '2020', '2021', '2022', '2023'):
    folder = f'./nuinvest/{year}/acoes/'
    for file in os.listdir(folder):
        for trade in [ Trade(extracted) for extracted in read_table(f'{folder}{file}') ]:
            #print(file, ' ==> ', trade)
            stock = Stock(trade.ticker)
            idx = result.index(stock) if stock in result else None
            if idx:
                stock = result[idx]
            else:
                result.append(stock)
            stock.addTrade(trade)

[print(x) for x in result]