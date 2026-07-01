from operator import not_
from sys import exception
import streamlit as st
import pandas as pd
import numpy as np
from argoapi import Argoquery
from teiaapi import Teiaquery
import requests

st.title("CONSULTAR APIS")

# Inicializa o estado se não existir
if 'resultados_argo' not in st.session_state:
    st.session_state.resultados_argo = None
if 'resultados_teia' not in st.session_state:
    st.session_state.resultados_teia = None


col1, col2 = st.columns(2)
with col1:
    data_input = st.text_input("Digite a data (ddMMaaaa): ",key="data")

with col2:
    nsu_input = st.text_input("Digite o número da NSU: ",key="nsu")

coluna01, coluna02 = st.columns(2)
with coluna01:
    btn_consultar_argo = st.button("CONSULTAR API ARGO")
    if  btn_consultar_argo:
        if data_input and nsu_input:
            try:
                with st.spinner("Consultando API"):
                    queryargo = Argoquery(data_input,nsu_input )
                    # lista_resultados_argo = queryargo.query_nsu()  
                    st.session_state.resultados_argo = queryargo.query_nsu()
            
                if st.session_state.resultados_argo:
                    st.success(f"Foi encontrado {len(st.session_state.resultados_argo)} registro (s) - API Argo")
                    # for item in st.session_state.resultados_argo:
                    #     st.json(item)
                else:
                    st.error("NSU não localizada! - API Argo")

            except requests.exceptions.HTTPError as errh:
                st.error(f"Erro de conexão com o servidor: {errh}")
            except ValueError:
                st.error("Erro ao processar dados: O servidor retornou uma resposta inválida. Tente novamente em instantes.")
            except Exception as e:
                st.error(f"Erro inesperado: {e}")

        else:   
            st.warning(f"Por favor, preencha corretamente os campos de DATA e NSU!")

with coluna02:
    btn_consultar_teia = st.button("CONSULTAR API TEIA")
    if  btn_consultar_teia:
        if data_input and nsu_input:
            try:
                with st.spinner("Consultando API"):
                    queryteia = Teiaquery(data_input,nsu_input )
                    # lista_resultados_teia = queryteia.query_nsu()  
                    st.session_state.resultados_teia = queryteia.query_nsu()
            
                if st.session_state.resultados_teia:
                    st.success(f"Foi encontrado {len(st.session_state.resultados_teia)} registro (s) - API Argo")
                    # for item in st.session_state.resultados_teia:
                    #     st.json(item)
                else:
                    st.error("NSU não localizada! - API Teia")

            except requests.exceptions.HTTPError as errh:
                st.error(f"Erro de conexão com o servidor: {errh}")
            except ValueError:
                st.error("Erro ao processar dados: O servidor retornou uma resposta inválida. Tente novamente em instantes.")
            except Exception as e:
                st.error(f"Erro inesperado: {e}")

        else:   
            st.warning(f"Por favor, preencha corretamente os campos de DATA e NSU!")


    # coluna01, coluna02 = st.columns(2)


# Exibição (Sempre exibe se houver dados no session_state)
col_res_1, col_res_2 = st.columns(2)

with col_res_1:
    if st.session_state.resultados_argo:
        st.subheader("Resultado Argo")
        for item in st.session_state.resultados_argo:
            st.json(item)

with col_res_2:
    if st.session_state.resultados_teia:
        st.subheader("Resultado Teia")
        for item in st.session_state.resultados_teia:
            st.json(item)