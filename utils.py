import streamlit as st
from dataset import df
import pandas as pd
import time


def format_number(value, prefix=''):
    for unit in ['', 'mil']:
        if value < 1000:
            return f'{prefix}{value:.2f}{unit}'

        value /= 1000
    return f'{prefix}{value:.2f} milhões'

# O for unit in ['', 'mil']: percorre duas opções de sufixo:

# '' → sem unidade (valor normal).
# 'mil' → milhares.

# Se o número for menor que 1000, mostra ele normal.
# Se for maior que 1000, divide por 1000 e mostra   em mil.
# Se ainda for muito grande (passou de mil duas vezes), mostra em milhões.
# O prefix serve para colocar algo antes, tipo "R$".

# Exemplos:
# format_number(500, 'R$') → R$500.00
# format_number(2500, 'R$') → R$2.50mil
# format_number(5_000_000, 'R$') → R$5.00 milhões

# Criando df_receita_estado
#['Preco'] (simples) → resultado é uma Series.
#[['Preco']] (duplo) → resultado é um DataFrame.
# Isso importa dependendo do que você vai fazer depois:
# Se precisa de uma tabela (ex.: para gráficos no Streamlit), o DataFrame é mais conveniente.
# Se só quer os valores como vetor, a Series já basta.


# DataFrame Receita por Local
# 1. Receita por local

# Com `as_index=False`**
#   A coluna usada no `groupby` continua sendo uma **coluna normal** no DataFrame:
df_rec_estado = df.groupby('Local da compra', as_index=False)[['Preco']].sum()

# 2. Coordenadas únicas
df_coords = df.drop_duplicates(subset=['Local da compra'])[['Local da compra', 'lat', 'lon']]

# 3. Merge das duas tabelas
df_rec_estado = (
    df_coords.merge(df_rec_estado, on='Local da compra')
             .sort_values('Preco', ascending=False)
)


# DataFrame Recita Mensal

# Está colocando a coluna 'Data da Compra' como índice, agrupando por mês e somando os valores da coluna 'Preco'
df_rec_mensal = (
    df
    .set_index('Data da Compra') # Define a coluna 'Data da Compra' como índice
    .groupby(pd.Grouper(freq='ME'))['Preco'] # Agrupa os dados por mês usando o índice de datas
    .sum() # Soma os valores da coluna 'Preco' em cada mês
    .reset_index() # Reseta o índice para voltar a ter uma coluna 'Data da Compra'
)

# Criando uma coluna com o ano e mês
df_rec_mensal['Ano'] = df_rec_mensal['Data da Compra'].dt.year
df_rec_mensal['Mes'] = df_rec_mensal['Data da Compra'].dt.month_name()

# DataFrame Recita por categoria

df_rec_categoria = df.groupby('Categoria do Produto')[['Preco']].sum().sort_values('Preco', ascending=False)

# DtaFrame Vendedores

df_vendedores = df.groupby('Vendedor')['Preco'].agg(['sum', 'count'])

# Função para converter em arquivo csv

#Quando você coloca @st.cache_data em cima de uma função:
    # O Streamlit executa a função uma vez e guarda o resultado.
    # Nas próximas execuções, se os argumentos da função não mudarem, ele não roda de novo: apenas retorna o resultado guardado.
    # Isso deixa a aplicação muito mais rápida, porque evita recarregar ou recalcular dados pesados (como ler um CSV grande,
    # consultar uma API, ou processar um DataFrame).

#@st.cache_data → usado para dados (DataFrames, listas, resultados de cálculos).
#@st.cache_resource → usado para recursos (objetos pesados que devem ser criados uma vez, como conexões de banco,
# modelos de ML, clientes de API).

@st.cache_data
def converter_csv(df):
    return df.to_csv(index=False).encode('utf-8')

def mensagem_sucesso():
    success = st.success(
        'Arquivo baixado com sucesso',
        icon = '✅'
    )
    time.sleep(3)
    success.empty()

