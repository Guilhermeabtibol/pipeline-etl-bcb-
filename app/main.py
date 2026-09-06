from app.export import export_to_excel
from app.extract import fetch_bcra_data
from app.load import load_to_mysql
from app.transform import transform_economic_data


def run_pipeline():
    print("🚀 Iniciando Pipeline ETL...")

    # 1. Extract
    raw_data = fetch_bcra_data()

    if raw_data.empty:
        print(
            "[ERRO] Não foi possível extrair dados de nenhuma fonte. Encerrando."
        )
        return

    # 2. Transform
    df_clean = transform_economic_data(raw_data, indicador_nome="USD/BRL")

    # 3. Load (MySQL)
    try:
        engine = create_engine(DATABASE_URL)
        load_to_mysql(df_clean, engine=engine)
    except Exception as e:
        print(f"[ERRO - MAIN] Falha ao conectar ao banco de dados: {e}")

    # 4. Export (Excel)
    excel_file = export_to_excel(df_clean)
    print(f"✅ Excel gerado com sucesso em: {excel_file}")


if __name__ == "__main__":
    run_pipeline()