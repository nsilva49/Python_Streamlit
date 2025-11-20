import streamlit as st
from dataset import df
import pandas as pd
from utils import converter_csv, mensagem_sucesso


st.title('Dataset de Vendas')

# Listando as colunas do df

#Segundo argumento (options) → é a lista de opções que o usuário pode escolher.
#Terceiro argumento (default) → define quais dessas opções já vêm selecionadas quando o componente aparece.
with st.expander('colunas'):
    colunas = st.multiselect(
        'Selecione as Colunas',
        list(df.columns),
        list(df.columns)
    )
# Listando as linhas
st.sidebar.title('Filtros')
with st.sidebar.expander('Categoria do Produto'):
    categorias = st.multiselect(
        'Selecione as Categorias',
        df['Categoria do Produto'].unique(),
        df['Categoria do Produto'].unique()

    )

# slider é um janela deslizante onde pode selecionar um intervalo de valor
with st.sidebar.expander('Preço do Produto'):
    preco = st.slider(
        'Selecione o Preço',
        0, 5000, # valores mínimo e máximo
        (0, 5000) # valor inicial selecionado. Como está em formato de tupla, o slider
        # vira um intervalo (range slider), permitindo escolher dois valores: preço mínimo e preço máximo

    )

with st.sidebar.expander('Data da Compra'):
    data_compra = st.date_input(
        'Selecione a Data',
        (df['Data da Compra'].min(),
        df['Data da Compra'].max())
    )
 # Converter para Timestamp para comparar corretamente
#data_compra = tuple(pd.to_datetime(data_compra))

# Criando a query

#Em Python, query = consulta.
#Pode ser usada para filtrar dados (Pandas), consultar banco de dados (SQL), ou buscar informações (APIs).

# `Categoria do Produto` in @categorias -  coluna do df é Categoria do Produto e @categorias é a variável
#onde será armazenada os valores
# @preco[0] <= Preço <= @preco[1] - preço mínimo [0] e máximo[1]

query = (
    "`Categoria do Produto` in @categorias and "
    "@preco[0] <= `Preco` <= @preco[1] and "
    "@data_compra[0] <= `Data da Compra` <= @data_compra[1]"
)


# Filtrando as linhas do DataFrame
filtro_dados = df.query(query)

# Filtrando pelas colunas selecionadas
filtro_dados = filtro_dados[colunas]

# Exibindo no Streamlit
st.dataframe(filtro_dados)

# Mostrar dimensões

#.shape é um atributo do DataFrame que retorna uma tupla (n_linhas, n_colunas).
# filtro_dados.shape[0] → número de linhas.
# filtro_dados.shape[1] → número de colunas.
# :blue[...] - É uma sintaxe especial do Streamlit para aplicar cor ao texto
st.markdown(f'A tabela possui :blue[{filtro_dados.shape[0]}] linhas e :blue[{filtro_dados.shape[1]}] colunas')

st.markdown('Escreva o nome do Arquivo')

coluna1, coluna2 = st.columns(2)
with coluna1:
    nome_arquivo = coluna1.text_input(
        '',
        label_visibility = 'collapsed' #oculta completamente o label, deixando só a caixa de texto visível.
    )
    nome_arquivo += '.csv' # para concatenar o nome do arquivo com .csv

with coluna2:
    st.download_button(
        'Baixar o arquivo',
        data = converter_csv(filtro_dados),
        file_name= nome_arquivo,
        mime = 'text/csv', # o tipo de arquivo
        on_click = mensagem_sucesso # o que será mostrado ao clicar
    )



