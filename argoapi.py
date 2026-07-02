import os 
import sys
import json
import shutil
import requests
from datetime import datetime, date, timedelta
from time import time, sleep
import pytz
from requests.adapters import HTTPAdapter
from urllib3.util import Retry
import streamlit as st

class Argoquery():
    def __init__(self,str_dtInicial,nsu):
        self.urlauth = st.secrets["api_argo"]["ARGO_URL_AUTH"]    
        self.login = st.secrets["api_argo"]["ARGO_LOGIN"]
        self.password = st.secrets["api_argo"]["ARGO_PASSWORD"]
        self.apirota = st.secrets["api_argo"]["ARGO_URL_API"]
        self.vendas_cartoes = f'transacoescartoes?dataInicial={str_dtInicial}&datafinal={str_dtInicial}'
        self.nsu = str(nsu).strip()
        self.session = self.configure_resilient_session()

    @staticmethod
    def configure_resilient_session() -> requests.Session:
        session = requests.Session()
        retries = Retry(
            total=5,
            backoff_factor=3,  # 3s, 6s, 12s, 24s...
            status_forcelist=[429, 500, 502, 503, 504,524],
            raise_on_status=False  # Permite tratar os status manualmente no fluxo
        )
        adapter = HTTPAdapter(max_retries=retries)
        session.mount("https://", adapter)
        session.mount("http://", adapter)
        return session

    def credential_connection(self):
        rPost = self.session.post(
        self.urlauth,
        json={"login": self.login,
              "password": self.password
              }
        )
        token = rPost.json()['access_token']
        headers = {"Authorization": f"Bearer {token}"}
        return headers

    def api_connection(self):
        urlcompleta= f"{self.apirota}{self.vendas_cartoes}"
        response = self.session.get(urlcompleta,headers=self.credential_connection(),timeout=60)
        dadosvenda = response.json()          
        return dadosvenda

    def query_nsu(self):
        nsu_alvo = self.nsu
        vendas = self.api_connection()
        dadosencontrados = []
        for venda in vendas:
            if venda.get("nsu") == nsu_alvo or venda.get("nsu").endswith(nsu_alvo) :
                info_simplificada ={
                    "empresa":venda.get("idempresa"),
                    "loja":venda.get("idempresa"),
                    "datavenda":venda.get("datavenda"),
                    "nsu":venda.get("nsu"),
                    "valorbruto":venda.get("valorbruto"),
                    
                    # "horavenda":venda.get("horavenda")
                }
                dadosencontrados.append(info_simplificada)

        return dadosencontrados


# query = Argoquery(24062026,200)

# # print(query.query_nsu())
# for i in query.query_nsu():
#     print(i)