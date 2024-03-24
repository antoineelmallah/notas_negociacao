import os

def iterate(root_path, predicate, callback):
    for root, _, files in os.walk(root_path):
        if predicate(root):
            for file in files:
                callback(f'{root}/{file}')

#iterate('/home/mallah/Documents/notas_negociacao/ativos', lambda file : file.endswith('acoes'), lambda file : print(file))