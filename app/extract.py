import requests
import pandas as pd
from datetime import datetime

def fetch_bcra_data(codigo_serie: int = 10813) -> pd.DataFrame:
    """
    Tenta buscar os dados do Banco Central. Se falhar por erro HTTP (ex: 406/502),
    faz fallback direto para a AwesomeAPI sem quebrar a execução.
    """
    url = f"https://api.bcb.gov.br/dados/serie/bcdata.sgs.{codigo_serie}/dados?formato=json"
    headers = {
        "User-Agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
        "Accept": "application/json"
    }

    try:
        response = requests.get(url, headers=headers, timeout=5)
        response.raise_for_status()
        data = response.json()
        if isinstance(data, list) and len(data) > 0:
            df = pd.DataFrame(data)
            print(f"[EXTRACT] Extraídos {len(df)} registros brutos do BCB.")
            return df
    except Exception as e:
        print(f"[AVISO - EXTRACT] BCB indisponível ({e}).")

    print("[EXTRACT] Acionando Fallback: AwesomeAPI (USD-BRL)...")
    return fetch_awesomeapi_fallback()


def fetch_awesomeapi_fallback(dias: int = 30) -> pd.DataFrame:
    """
    API alternativa que retorna a cotação do dólar dos últimos N dias.
    """
    url = f"https://economia.awesomeapi.com.br/json/daily/USD-BRL/{dias}"
    try:
        response = requests.get(url, timeout=10)
        response.raise_for_status()
        data = response.json()
        
        registros = []
        for item in data:
            dt_obj = datetime.fromtimestamp(int(item["timestamp"]))
            registros.append({
                "data": dt_obj.strftime("%d/%m/%Y"),
                "valor": item["bid"]
            })
            
        df = pd.DataFrame(registros)
        print(f"[EXTRACT - FALLBACK] Extraídos {len(df)} registros da AwesomeAPI com sucesso.")
        return df
    except Exception as e:
        print(f"[ERRO CRÍTICO - EXTRACT] Falha ao consultar AwesomeAPI: {e}")
        return pd.DataFrame()