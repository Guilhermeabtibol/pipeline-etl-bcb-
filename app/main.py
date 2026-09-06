from app.database import get_engine
from app.extract import fetch_bcra_data
from app.transform import transform_economic_data
from app.load import load_to_mysql

def run_pipeline():
    print("--------------------------------------------------")
    print("🚀 INICIANDO PIPELINE ETL DE INDICADORES FINANCEIROS")
    print("--------------------------------------------------")
    
    engine = get_engine()

    # 1. Extração da cotação do Dólar (Série 10813)
    print("\n1. Extraindo cotação do Dólar (API BCB)...")
    raw_dolar = fetch_bcra_data(10813)

    # 2. Transformação dos dados
    print("\n2. Transformando e tratando os dados com Pandas...")
    df_dolar = transform_economic_data(raw_dolar, "USD_BRL")

    # Filtramos apenas os últimos 365 dias para a carga inicial ser ágil
    if not df_dolar.empty:
        df_dolar = df_dolar.tail(365)
        
        # 3. Carga no MySQL
        print("\n3. Gravando dados tratados no MySQL...")
        load_to_mysql(df_dolar, engine)

    print("\n--------------------------------------------------")
    print("✅ PIPELINE FINALIZADO COM SUCESSO!")
    print("--------------------------------------------------")

if __name__ == "__main__":
    run_pipeline()