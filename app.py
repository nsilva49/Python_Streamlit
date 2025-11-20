import streamlit as st
import plotly.express as px
from dataset import df
from utils import format_number
from graficos import grafico_map_estado, grafico_rec_mensal, grafico_rec_estado, \
    grafico_rec_categoria, grafico_vendedores, grafico_vendas_vendedor


# # Lista de Emojis Mais Utilizados

#  📊 Dashboards e Relatórios
# 📊  Gráfico de barras
# 📈  Gráfico de linha (crescimento)
# 📉  Gráfico de queda
# 📑  Documento / relatório
# 📋  Lista / checklist

#  💰 Vendas e Finanças
# 💰  Dinheiro / lucro
# 💵  Nota de dinheiro
# 💳  Cartão de crédito
# 🛒  Carrinho de compras
# 🛍️  Sacolas de compras
# 🏷️  Etiqueta / desconto
# 💲  Símbolo de dólar
#
#  🏢 Negócios e Trabalho
# 🏢  Empresa / escritório
# 👔  Profissional / negócios
# 🤝  Parceria / acordo
# 📦  Produto / estoque
# 🚚  Caminhão de entrega

#  ⚡ Destaques e Tendências
# ⭐  Destaque / favorito
# 🔥  Tendência / alta demanda
# ⚡  Rápido / performance
# ✅  Concluído / sucesso
# 🚀  Crescimento / expansão

st.set_page_config(layout="wide") # desloca o texto para esquerda
st.title('Dashboard de Vendas 🛒') # :shopping_trolley:  emoji de dashboard

# Adicionar filtros
st.sidebar.title('Filtro Vendedores')
filtro_vendedor = st.sidebar.multiselect(
    'Vendedores',
    df['Vendedor'].unique(),
)
if filtro_vendedor:
    df = df[df['Vendedor'].isin(filtro_vendedor)] # se o vendedor está em filtro_vendedor

# Criando abas
aba1, aba2, aba3 = st.tabs(['Dataset','Rceita','Vendedores'])

with aba1:
    st.dataframe(df)

with aba2:
    coluna1, coluna2 = st.columns(2)
    with coluna1:
       st.metric('Receita Total',format_number(df['Preco'].sum(), 'R$'))
       st.plotly_chart(grafico_map_estado, use_container_width=True)
       st.plotly_chart(grafico_rec_estado, use_container_width=True)

    with coluna2:
        st.metric('Quantidade de Vendas',format_number(df.shape[0])) #df.shape[0] → retorna o número de linhas do
        # DataFrame df. Cada linha normalmente representa uma venda, então isso equivale à
        # quantidade total de vendas registradas. Passa o índice 0, pois é a posição no df que irá
        # conter o valor tota de linhas quando coloca em ordem decrescente
        st.plotly_chart(grafico_rec_mensal, use_container_width=True) #ocupe automaticamente toda a largura do container
        st.plotly_chart(grafico_rec_categoria, use_container_width=True)

with aba3:
    coluna1, coluna2 = st.columns(2)
    with coluna1:
        st.plotly_chart(grafico_vendedores)
    with coluna2:
        st.plotly_chart(grafico_vendas_vendedor)