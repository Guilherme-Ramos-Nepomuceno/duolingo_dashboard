import streamlit as st
import pandas as pd
from io import StringIO

def texto_para_csv():
    st.title('Conversor de Texto para CSV')
    st.subheader("Como formatar seus dados:")
    st.code("ID_Cliente,Faixa_Etaria,Motivacao,Interesse_Idioma,Nivel_Atual\n"
            "1,25-34,Carreira,Inglês,Intermediário\n"
            "2,16-24,Cultura,Japonês,Iniciante", language=None)

    dados = st.text_area(
        "Cole seus dados aqui:",
        height=300,
        placeholder="Cole seus dados no formato mostrado acima..."
    )
    
    with st.expander("Opções avançadas"):
        tem_cabecalho = st.checkbox("Primeira linha contém cabeçalho", value=True)
        separador = st.selectbox("Separador de colunas", [",", ";", "|", "TAB"], index=0)
        nome_arquivo = st.text_input("Nome do arquivo", "dados.csv")
    
    separador = "\t" if separador == "TAB" else separador

    if st.button("Converter para CSV"):
        if not dados.strip():
            st.warning("Por favor, cole seus dados no campo acima")
            return
            
        try:
            linhas = dados.strip().split('\n')
            
            if tem_cabecalho:
                cabecalho = linhas[0].split(separador)
                dados_linhas = [linha.split(separador) for linha in linhas[1:]]
            else:
                cabecalho = [f"Coluna_{i+1}" for i in range(len(linhas[0].split(separador)))]
                dados_linhas = [linha.split(separador) for linha in linhas]
            
            df = pd.DataFrame(dados_linhas, columns=cabecalho)
            
            st.success("Conversão bem-sucedida! Visualização dos dados:")
            st.dataframe(df.head())
            
            csv = df.to_csv(index=False).encode('utf-8')
            
            st.download_button(
                label="📥 Baixar CSV",
                data=csv,
                file_name=nome_arquivo,
                mime='text/csv'
            )
            
        except Exception as e:
            st.error(f"Erro na conversão: {str(e)}")
            st.info("Verifique se todas as linhas têm o mesmo número de colunas")

if __name__ == "__main__":
    texto_para_csv()