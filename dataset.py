import json
import pandas as pd

file = open('dados/vendas.json')
data = json.load(file)
# print(data)

# Para abrir um arquivo json em formato de dataframe
df = pd.DataFrame.from_dict(data)

# Colocando a coluna data no formato dattime
df['Data da Compra'] = pd.to_datetime(df['Data da Compra'], format='%d/%m/%Y')

# Renomeando a coluna preco
df = df.rename(columns={'Pre\u00e7o': 'Preco'})
print(df)

file.close()
