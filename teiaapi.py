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


class Teiaquery():
    def __init__(self,str_data,nsu):
        self.urlbase = str('https://api.saferedi.nteia.com/v1/oauth/token') 
        self.client_id =  "2"
        self.client_secret =  "KZ00QSA1GPBqBlHsArhVlHLSyHTg6srmoqUCKb8c"
        self.grant_type = os.getenv("TEIA_GRANT")
        self.username = os.getenv("TEIA_USERNAME")
        self.password = os.getenv("TEIA_PASSWORD")
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
        url_completa = 'https://api.saferedi.nteia.com/v1/retorno/parcelas?tipo=venda&data=20260628'
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