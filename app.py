from operator import not_
from sys import exception
import streamlit as st
import pandas as pd
import numpy as np
from argoapi import Argoquery
from teiaapi import Teiaquery
import requests


# No topo do seu arquivo app.py
st.set_page_config(page_title="MR - Nexus API", page_icon="images/faviconmr.jpeg")

with st.sidebar:
    st.image("images/logomr.jpeg", width=160)
    st.markdown("---") # Linha separadora

# 2. Lógica de Validação de Acesso
def check_password():
    """Retorna True se o usuário passou pela autenticação."""
    
    def password_entered():
        # Obtém o dicionário de usuários e senhas do secrets.toml
        # Estrutura esperada: [users] -> chave = "senha"
        users = st.secrets.get("users", {})
        
        username = st.session_state.get("username", "")
        password = st.session_state.get("password", "")

        # Verifica se o usuário existe e se a senha está correta
        # .get() previne erro caso o usuário não exista no dicionário
        if username in users and users[username] == password:
            st.session_state["password_correct"] = True
            st.session_state["user_auth"] = username
            # Limpa os campos após login bem-sucedido
            del st.session_state["password"]
            del st.session_state["username"]
        else:
            st.session_state["password_correct"] = False

    # Verifica se já está autenticado
    if st.session_state.get("password_correct", False):
        return True

    # Formulário de Login (exibido apenas se não autenticado)
    st.title("🔐 Acesso Restrito")
    st.text_input("Usuário", key="username")
    st.text_input("Senha", type="password", key="password")
    
    if st.button("Entrar"):
        password_entered()
        st.rerun() # Atualiza a página para aplicar a mudança de estado
        
    return False

# --- FLUXO PRINCIPAL DO APP ---

if check_password():
    # O conteúdo principal da sua aplicação entra aqui
    st.success(f"Bem-vindo, {st.session_state['user_auth'].title()}!")
    
    # Exemplo de conteúdo protegido
    st.title("CONSULTAR APIS")

    # Inicializa o estado se não existir
    if 'resultados_argo' not in st.session_state:
        st.session_state.resultados_argo = None
    if 'resultados_teia' not in st.session_state:
        st.session_state.resultados_teia = None


    col1, col2, col3 = st.columns(3)
    with col1:
        data_input = st.text_input("Digite a data (ddMMaaaa): ",key="data")

    with col2:
        nsu_input = st.text_input("Digite o número da NSU: ",key="nsu")

    with col3:
        valor_input = st.text_input("Digite o número o valor bruto: ",key="valor")

    btn_query_both_apis = st.button("CONSULTAR AMBAS API(s)")

    if btn_query_both_apis:
        coluna01, coluna02 = st.columns(2)
        with coluna01:
            btn_consultar_argo = True
            if  btn_consultar_argo:
                if data_input and nsu_input:
                    try:
                        with st.spinner("Consultando API"):
                            queryargo = Argoquery(data_input,nsu_input, valor_input)
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


                elif data_input and valor_input:
                    try:
                        with st.spinner("Consultando API"):
                            queryargo = Argoquery(data_input,nsu_input,valor_input)
                            # lista_resultados_argo = queryargo.query_valor()  
                            st.session_state.resultados_argo = queryargo.query_valor()
                    
                        if st.session_state.resultados_argo:
                            st.success(f"Foi encontrado {len(st.session_state.resultados_argo)} registro (s) - API Argo")
                            # for item in st.session_state.resultados_argo:
                            #     st.json(item)
                        else:
                            st.error("VALOR não localizada! - API Argo")

                    except requests.exceptions.HTTPError as errh:
                        st.error(f"Erro de conexão com o servidor: {errh}")
                    except ValueError:
                        st.error("Erro ao processar dados: O servidor retornou uma resposta inválida. Tente novamente em instantes.")
                    except Exception as e:
                        st.error(f"Erro inesperado: {e}")

                else:   
                    st.warning(f"Por favor, Se possível Preencher o campo VALOR!")


        with coluna02:
            btn_consultar_teia = True
            if  btn_consultar_teia:
                if data_input and nsu_input:
                    try:
                        with st.spinner("Consultando API"):
                            queryteia = Teiaquery(data_input,nsu_input, valor_input)
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

                elif data_input and valor_input:
                    try:
                        with st.spinner("Consultando API"):
                            queryteia = Teiaquery(data_input,nsu_input, valor_input)
                            # lista_resultados_teia = queryteia.query_valor()  
                            st.session_state.resultados_teia = queryteia.query_valor()
                    
                        if st.session_state.resultados_teia:
                            st.success(f"Foi encontrado {len(st.session_state.resultados_teia)} registro (s) - API Argo")
                            # for item in st.session_state.resultados_teia:
                            #     st.json(item)
                        else:
                            st.error("VALOR não localizada! - API Teia")

                    except requests.exceptions.HTTPError as errh:
                        st.error(f"Erro de conexão com o servidor: {errh}")
                    except ValueError:
                        st.error("Erro ao processar dados: O servidor retornou uma resposta inválida. Tente novamente em instantes.")
                    except Exception as e:
                        st.error(f"Erro inesperado: {e}")

                else:   
                    st.warning(f"Por favor, preencher os campos NSU ou VALOR!")




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

    # Botão de Logout para encerrar sessão
    if st.sidebar.button("Sair"):
        st.session_state["password_correct"] = False
        st.rerun()

else:
    # Caso de erro de login
    if "password_correct" in st.session_state and not st.session_state["password_correct"]:
        st.error("Usuário ou senha incorretos.")




















