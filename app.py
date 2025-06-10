import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

@st.cache_data
def load_data():
    return pd.read_csv("data/duolingo.csv")

df = load_data()

st.title("Dashboard Duolingo")

st.subheader("Visualização da Base de Dados")
st.dataframe(df)

df_encoded = df.copy()
for col in df_encoded.select_dtypes(include='object').columns:
    df_encoded[col] = df_encoded[col].astype('category').cat.codes

st.subheader("Matriz de Correlação")
corr = df_encoded.corr()
fig, ax = plt.subplots()
im = ax.imshow(corr, interpolation='none')
ax.set_xticks(range(len(corr.columns)))
ax.set_yticks(range(len(corr.columns)))
ax.set_xticklabels(corr.columns, rotation=45, ha='right')
ax.set_yticklabels(corr.columns)
fig.colorbar(im, ax=ax)
st.pyplot(fig)

def plot_count(x, y, title):
    tab = df.groupby([x, y]).size().unstack(fill_value=0)
    st.subheader(title)
    st.bar_chart(tab)

# Gráficos solicitados
plot_count('Faixa_Etaria', 'Motivacao', 'Faixa Etária vs Motivação')
plot_count('Orcamento_Mensal', 'Nivel_Atual', 'Orçamento Mensal vs Nível Atual')
plot_count('Horario_Estudo', 'Faixa_Etaria', 'Horário de Estudo vs Faixa Etária')
plot_count('Motivacao', 'Nivel_Atual', 'Motivação vs Nível Atual')
plot_count('Ocupacao', 'Interesse_Idioma', 'Ocupação vs Interesse de Idioma')
plot_count('Rede_Social', 'Faixa_Etaria', 'Rede Social vs Faixa Etária')
plot_count('Rede_Social', 'Nivel_Atual', 'Rede Social vs Nível Atual')

