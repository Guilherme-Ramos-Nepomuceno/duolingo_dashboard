import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

# 1. Carrega a tabela
@st.cache_data
def load_data(path="data/duolingo.csv"):
    return pd.read_csv(path)

df = load_data()

# 2. Define regras de perfil
profiles_rules = {
    'Carreirista Tech': lambda r: (
        r['Ocupacao'] in ['Tecnologia', 'Empreendedor', 'Outras_Areas'] and
        r['Interesse_Idioma'] in ['Ingles', 'Alemao'] and
        r['Rede_Social']=='LinkedIn' and
        r['Orcamento_Mensal'] in ['Acima_500','301-500', '151-300']
    ),
    'Jovem Cultural': lambda r: (
        r['Motivacao'] in ['Cultura','Estudos'] and
        r['Rede_Social'] in ['TikTok','Instagram', 'LinkedIn'] and
        r['Orcamento_Mensal'] in ['Ate_150', '151-300', '301-500'] and
        r['Interesse_Idioma'] in ['Ingles', 'Japones', 'Frances', 'Espanhol']
    ),
    'Viajante Experiente': lambda r: (
        r['Motivacao']=='Viagens' and
        r['Interesse_Idioma'] in ['Ingles', 'Frances', 'Espanhol', 'Italiano'] and
        r['Orcamento_Mensal'] in ['Ate_150', '151-300', '301-500', 'Acima_500'] and
        r['Rede_Social'] in ['Facebook','Instagram', 'TikTok']
        ),
    'Desenvolvedor Pessoal': lambda r: (
        r['Motivacao']=='Viagens',
        r['Interesse_Idioma'] in ['Ingles', 'Frances', 'Espanhol', 'Italiano'],
        r['Orcamento_Mensal'] in ['Ate_150', '151-300', '301-500', 'Acima_500'],
        r['Rede_Social'] in ['Facebook','Instagram', 'TikTok'],
        r['Faixa_Etaria'] in [ '25-34', '45+']
    )
}

# 3. Classifica cada linha

def classify(row):
    for name, rule in profiles_rules.items():
        if rule(row):
            return name
    return 'Outro'

df['Perfil'] = df.apply(classify, axis=1)

# 4. Descrições dos perfis
descricoes = {
    'Carreirista Tech': 'Profissional focado em crescimento, com alto poder aquisitivo e necessidade imediata do idioma para o trabalho.',
    'Jovem Cultural': 'Estudante motivado por hobbies e cultura pop, altamente conectado em redes sociais visuais e com orçamento limitado.',
    'Viajante Experiente': 'Adulto que busca o idioma para enriquecer suas experiências de viagem, com flexibilidade de horários.',
    'Desenvolvedor Pessoal': 'Público maduro que aprende por prazer e desenvolvimento intelectual, sem pressão profissional.',
    'Outro': 'Perfis diversos não enquadrados nas categorias principais.'
}

# 5. Funções de plotagem

def bar(ax, s, title, percent=False):
    vc = s.value_counts(normalize=percent)
    vals = vc.values * (100 if percent else 1)
    ax.bar(vc.index.astype(str), vals)
    ax.set_title(title)
    ax.set_xticklabels(vc.index.astype(str), rotation=45, ha='right')
    ax.set_ylabel('%' if percent else 'Count')


def pie(ax, s, title):
    vc = s.value_counts(normalize=True)
    vals = vc.values * 100
    ax.pie(vals, labels=vc.index, autopct='%1.0f%%')
    ax.set_title(title)
    ax.axis('equal')

# 6. Dashboard
st.title('Dashboard Duolingo por Perfil')
for perfil in list(profiles_rules.keys()):
    dfp = df[df['Perfil']==perfil]
    total = len(dfp)
    st.markdown('---')
    st.subheader(f"{perfil} — {total} usuários")
    st.write(descricoes[perfil])

    fig, axs = plt.subplots(2, 3, figsize=(14,8))
    # Faixa Etária
    bar(axs[0,0], dfp['Faixa_Etaria'], 'Faixa Etária', percent=True)
    # Motivação
    bar(axs[0,1], dfp['Motivacao'], 'Motivação', percent=True)
    # Idioma
    pie(axs[0,2], dfp['Interesse_Idioma'], 'Idiomas')
    # Orçamento
    bar(axs[1,0], dfp['Orcamento_Mensal'], 'Orçamento Mensal', percent=True)
    # Rede Social
    pie(axs[1,1], dfp['Rede_Social'], 'Rede Social')
    # Nível Atual
    bar(axs[1,2], dfp['Nivel_Atual'], 'Nível Atual', percent=True)

    st.pyplot(fig)

# Fim
