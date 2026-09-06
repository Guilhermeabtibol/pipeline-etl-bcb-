import requests
import pandas as pd
from datetime import datetime, timedelta

def fetch_bcra_data(codigo_serie: int = 10813) -> pd.DataFrame:
    """
    Tenta consumir a API do Banco Central do Brasil.
    Se o BCB estiver fora do ar (Erro 502/503), faz fallback automático para a AwesomeAPI.
    """
    url = f"https://api.bcb.gov.br/dados/serie/bcdata.sgs.{codigo_serie}/dados?formato=json"
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
    }

    try:
        response = requests.get(url, headers=headers, timeout=10)
        response.raise_for_status()
        data = response.json()
        df = pd.DataFrame(data)
        print(f"[EXTRACT] Extraídos {len(df)} registros brutos do BCB (série {codigo_serie}).")
        return df
    except requests.RequestException as e:
        print(f"[AVISO - EXTRACT] Falha no BCB (Série {codigo_serie}): {e}")
        
        # Tenta série alternativa do BCB
        if codigo_serie == 10813:
            print("[EXTRACT] Tentando série alternativa do BCB (Série 1)...")
            return fetch_bcra_data(1)
            
        # Se ambas do BCB falharem, aciona a API secundária (AwesomeAPI)
        print("[EXTRACT] BCB indisponível. Acionando Fallback: AwesomeAPI (USD-BRL)...")
        return fetch_awesomeapi_fallback()


def fetch_awesomeapi_fallback(dias: int = 30) -> pd.DataFrame:
    """
    API alternativa para extração de cotação do Dólar caso o BCB esteja inacessível.
    Retorna no mesmo formato esperado pelo BCB: colunas ['data', 'valor'].
    """
    url = f"https://economia.awesomeapi.com.br/json/daily/USD-BRL/{dias}"
    try:
        response = requests.get(url, timeout=10)
        response.raise_for_status()
        data = response.json()
        
        registros = []
        for item in data:
            # Converte timestamp UNIX para data dd/mm/YYYY
            dt_obj = datetime.fromtimestamp(int(item["timestamp"]))
            registros.append({
                "data": dt_obj.strftime("%d/%m/%Y"),
                "valor": item["bid"]
            })
            
        df = pd.DataFrame(registros)
        print(f"[EXTRACT - FALLBACK] Extraídos {len(df)} registros da AwesomeAPI com sucesso.")
        return df
    except requests.RequestException as e:
        print(f"[ERRO - EXTRACT] Falha crítica em todas as fontes de dados: {e}")
        return pd.DataFrame()