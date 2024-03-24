import pandas as pd
from iterate_over_files import iterate

dfs = []

def callback(path):
    dfs.append(pd.read_excel(path))

iterate('./xls', lambda path : True, callback)

df = pd.concat(dfs, axis='rows')

print(df.columns)

group = df.groupby('Código de Negociação')['Quantidade (Líquida)', 'Preço Médio (Compra)']

print(group)
