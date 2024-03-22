import pdfquery
from iterate_over_files import iterate
from model import Trade, Stock


def get_box_positions_between_texts(pdf: pdfquery.PDFQuery, common_value_field):
    return [(0.0, float(item.attrib['y0']), 600.0, float(item.attrib['y1'])) for item in pdf.pq(f'LTTextLineHorizontal:contains("{ common_value_field }")')]


def read_table(path):
    pdf = pdfquery.PDFQuery(path)

    pdf.load()
 
    limits = get_box_positions_between_texts(pdf, 'BOVESPA')

    return [ pdf.pq('LTTextLineHorizontal:overlaps_bbox("%s, %s, %s, %s")' % line).text() for line in limits]


result = []

def callback(path):
    for trade in [ Trade(extracted) for extracted in read_table(path) ]:
        stock = Stock(trade.ticker)
        if stock in result:
            stock = result[result.index(stock)]
        else:
            result.append(stock)
        stock.addTrade(trade)


iterate('/home/mallah/Documents/notas_negociacao/ativos', lambda path : path.endswith('acoes'), callback)

[print((x.ticker, x.average_price())) for x in result]