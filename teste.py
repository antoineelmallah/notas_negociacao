import pdfquery
import os
from enum import Enum
import re

def get_box_positions_between_texts(pdf, superior, inferior):
    superior_box = pdf.pq(f'LTTextBoxHorizontal:contains("{superior}")')
    inferior_box = pdf.pq(f'LTTextBoxHorizontal:contains("{inferior}")')
    y0 = float(inferior_box.attr('y1'))
    y1 = float(superior_box.attr('y0'))
    return (0, y0, 2000, y1)

def read_table(path):

    pdf = pdfquery.PDFQuery(path)

    pdf.load()

    pdf.tree.write('rico-tree.txt', pretty_print=True)

#    limits = get_box_positions_between_texts(pdf, 'Mercado', 'Resumo dos Negócios')

#    result = pdf.pq('LTTextLineHorizontal:in_bbox("%s, %s, %s, %s")' % limits)

#    print([i for i in result.items()])
#    print([i.text() for i in result.parent().items()])

#    return result.text()

year = 2020
file = 'Invoice_3724.pdf'

file_path = f'./nuinvest/{year}/acoes/{file}'

print(read_table('/home/mallah/Documents/notas_negociacao/RICO/XPINC_NOTA_NEGOCIACAO_B3_5_2022.pdf'))

