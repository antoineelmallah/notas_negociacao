import pdfquery
import os
from enum import Enum
import re

#file = '/home/mallah/Documents/notas_negociacao/RICO/XPINC_NOTA_NEGOCIACAO_B3_5_2022.pdf'
file = '/home/mallah/Downloads/nuinvest/2021/acoes/Invoice_119107.pdf'

pdf = pdfquery.PDFQuery(file)

pdf.load()
'''
pages= pdf.pq(f'LTTextBoxHorizontal:contains("1-BOVESPA")').parents(f'LTPage:contains("1-BOVESPA")')
result = []
for page in pages:
    boxes = pdf.pq(f'LTPage[page_index="{page.layout.pageid - 1}"] LTTextBoxHorizontal:contains("1-BOVESPA") *').items()
    for box in boxes:
        print(box)
        y0 = float(box.attr('y0'))
        y1 = float(box.attr('y1'))
        result.append((0, y0, 2000, y1))

#print(result)
'''
boxes = [(0.0, float(item.attrib['y0']), 600.0, float(item.attrib['y1'])) for item in pdf.pq(f'LTTextLineHorizontal:contains("BOVESPA")')]

for box in boxes:
    print('==================================================================')
    for x in pdf.pq('LTTextLineHorizontal:overlaps_bbox("%s, %s, %s, %s")' % box).items():
        print('-----------------------------------------------------------------')
        print(x.text())
'''

def get_box_positions_between_texts(pdf: pdfquery.PDFQuery, superior, inferior):
    pages= pdf.pq(f'LTTextBoxHorizontal:contains("{superior}")').parents(f'LTPage:contains("{superior}")')
    result = []
    for page in pages:
        superior_box = pdf.pq(f'LTPage[page_index="{page.layout.pageid - 1}"] LTTextBoxHorizontal:contains("{superior}")')
        inferior_box = pdf.pq(f'LTPage[page_index="{page.layout.pageid - 1}"] LTTextBoxHorizontal:contains("{inferior}")')
        y0 = float(inferior_box.attr('y1'))
        y1 = float(superior_box.attr('y0'))
        result.append((0, y0, 2000, y1))

    return result

def read_table(path):

    pdf = pdfquery.PDFQuery(path)

    pdf.load()

    pdf.tree.write('rico-tree.txt', pretty_print=True)

    #limits = get_box_positions_between_texts(pdf, 'Mercado', 'Resumo dos Negócios')

    #result = pdf.pq('LTTextLineHorizontal:in_bbox("%s, %s, %s, %s")' % limits)

    result = []

    for limits in get_box_positions_between_texts(pdf, 'BOVESPA', 'Resumo dos Neg'):
    
        r = pdf.pq('LTTextLineHorizontal:in_bbox("%s, %s, %s, %s")' % limits)
        result.append(r)

        print([i for i in r.items()])
        print([i.text() for i in r.parent().items()])

    return result

print(read_table('/home/mallah/Documents/notas_negociacao/RICO/XPINC_NOTA_NEGOCIACAO_B3_5_2022.pdf'))

'''