import os 
import sys
import json
import shutil
from numpy.char import endswith
import requests
from datetime import datetime, date, timedelta
from time import time, sleep
import pytz
from requests.adapters import HTTPAdapter
from urllib3.util import Retry
import streamlit as st

class Teiaquery():
    def __init__(self,str_data,nsu):
        self.urlbase = st.secrets["api_teia"]["TEIA_URL_BASE"]
        self.client_id = st.secrets["api_teia"]["TEIA_CLIENTE_ID"]
        self.client_secret = st.secrets["api_teia"]["TEIA_CLIENTE_SECRET"]
        self.grant_type = st.secrets["api_teia"]["TEIA_GRANT"]
        self.username = st.secrets["api_teia"]["TEIA_USERNAME"]
        self.password = st.secrets["api_teia"]["TEIA_PASSWORD"]
        self.str_data = str_data
        self.nsu = str(nsu)

    def credential_connection(self):
        rPost = requests.post(self.urlbase,
        json={
            "client_id": self.client_id,
            "client_secret": self.client_secret,
            "grant_type": self.grant_type,
            "username": self.username,
            "password": self.password
        }
        )
        rPost.raise_for_status()
        token = rPost.json()['access_token']
        headers = {"Authorization": f"Bearer {token}"}
     
        return headers
    
            
    def api_connection(self):
        data_dt = datetime.strptime(self.str_data, "%d%m%Y")    
        data_amanha = data_dt + timedelta(days=1) 
        data_formatada = data_amanha.strftime("%Y%m%d")
        url_base = st.secrets["api_teia"]["TEIA_URL_COMPLETA"] 
        if not url_base.endswith("="):
            url_completa = f"{url_base}{data_formatada}"
        else:
            url_completa = f"{url_base}{data_formatada}"
        headers = self.credential_connection()
        response = requests.get(url_completa,headers=headers,timeout=40)
        dadosvenda = response.json()
        
        return dadosvenda

    def query_nsu(self):
        nsualvo = self.nsu
        dadosvenda = self.api_connection()
        registros_localizados = []

        listavendas = dadosvenda.get("data",[])
        for item in listavendas:
            info_vendas = item.get("venda",{})
            valor_nsu = info_vendas.get("nsu")

            info_simplificada ={
                "empresa":info_vendas.get("empresa_codigo"),
                "loja":info_vendas.get("loja_codigo"),
                "datavenda":info_vendas.get("venda_data"),
                "nsu":valor_nsu,
                "valorbruto":item.get("valor_bruto")
            }

            if valor_nsu is not None:
                nsu_str = str(valor_nsu)
                if nsu_str == nsualvo or nsu_str.endswith(nsualvo):
                    registros_localizados.append(info_simplificada)     

        return registros_localizados


# query = Teiaquery(28062026,544)
# resultado = query.query_nsu()
# print(resultado)

# --- Iniciando Processamento | Empresa: 15 | Data: 20260628 ---
# https://api.saferedi.nteia.com/v1/retorno/parcelas?tipo=venda&data=20260628&empresa_codigo=15
# Empresa 15
# Execução concluída em: 0 minutos e 2 segundos
# Empresa Id 35