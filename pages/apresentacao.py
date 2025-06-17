import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

# 1. Carregamento de dados
@st.cache_data
def load_data(path="data/duolingo.csv"):
    return pd.read_csv(path)

df = load_data()

# 2. Classificação de perfis

def classificar_perfil(row):
    if (
        row['Ocupacao'] == 'Tecnologia'
        and row['Interesse_Idioma'] == 'Ingles'
        and row['Rede_Social'] == 'LinkedIn'
    ):
        return 'Carreirista Tech'
    elif (
        row['Motivacao'] in ['Cultura', 'Estudos']
        and row['Rede_Social'] in ['Instagram', 'TikTok']
    ):
        return 'Jovem Cultural'
    elif row['Motivacao'] == 'Viagens':
        return 'Viajante Experiente'
    elif (
        row['Faixa_Etaria'] == '45+'
        or (row['Rede_Social'] == 'Facebook' and row['Motivacao'] in ['Desenvolvimento', 'Carreira'])
    ):
        return 'Desenvolvedor Pessoal'
    else:
        return 'Outro'

# Aplicar classificação
if 'Perfil' not in df.columns:
    df['Perfil'] = df.apply(classificar_perfil, axis=1)

# 3. Dicionário de descrições
descricoes = {
    'Carreirista Tech': 'Profissional focado em crescimento, com alto poder aquisitivo e necessidade imediata do idioma para o trabalho.',
    'Jovem Cultural': 'Estudante motivado por hobbies e cultura pop, altamente conectado em redes sociais visuais e com orçamento limitado.',
    'Viajante Experiente': 'Adulto que busca o idioma para enriquecer suas experiências de viagem, com flexibilidade de horários.',
    'Desenvolvedor Pessoal': 'Público maduro que aprende por prazer e desenvolvimento intelectual, sem pressão profissional.',
    'Outro': 'Outros perfis não enquadrados nas categorias principais.'
}

# 4. Funções de plot

def plot_pie(ax, data, title):
    ax.pie(data.values, labels=data.index, autopct='%1.0f%%', startangle=90)
    ax.set_title(title)
    ax.axis('equal')


def plot_bar(ax, data, title):
    ax.bar(data.index.astype(str), data.values)
    ax.set_title(title)
    ax.set_ylabel('Quantidade')
    ax.set_xticklabels(data.index.astype(str), rotation=45, ha='right')

# 5. Layout no Streamlit
st.title('Dashboard Duolingo')
st.write('Última atualização: ...')

perfis = ['Carreirista Tech', 'Jovem Cultural', 'Viajante Experiente', 'Desenvolvedor Pessoal']

for i, perfil in enumerate(perfis):
    # Alterna cor de fundo com markdown
    if i % 2 == 0:
        st.markdown('---')
    else:
        st.markdown('')

    df_p = df[df['Perfil'] == perfil]
    count = len(df_p)

    # Header com nome e descrição
    col1, col2 = st.columns([1, 3])
    with col1:
        st.subheader(f"{perfil}")
        st.metric(label="Total", value=count)
    with col2:
        st.write(descricoes.get(perfil, ''))

    # Quatro gráficos
    fig, axes = plt.subplots(1, 4, figsize=(16, 3))

    # Gráfico 1: faixa/área/motivação
    if perfil == 'Carreirista Tech':
        key = 'Ocupacao'
        title1 = 'Área de atuação'
    elif perfil == 'Jovem Cultural':
        key = 'Motivacao'
        title1 = 'Motivação'
    else:
        key = 'Faixa_Etaria'
        title1 = 'Faixa Etária'
    data1 = df_p[key].value_counts()
    plot_bar(axes[0], data1, title1)

    # Gráfico 2: Idiomas/Interesse
    lang_key = 'Interesse_Idioma'
    data2 = df_p[lang_key].value_counts()
    plot_pie(axes[1], data2, 'Idiomas')

    # Gráfico 3: Orçamento Mensal
    orc_key = 'Orcamento_Mensal'
    data3 = df_p[orc_key].value_counts().sort_index()
    plot_bar(axes[2], data3, 'Orçamento Mensal')

    # Gráfico 4: Rede Social
    soc_key = 'Rede_Social'
    data4 = df_p[soc_key].value_counts()
    plot_pie(axes[3], data4, 'Rede Social')

    st.pyplot(fig)

# FIM do dashboard
