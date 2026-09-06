import pandas as pd
from sqlalchemy import Engine

def load_to_mysql(df: pd.DataFrame, engine: Engine, table_name: str = "fato_indicadores_economicos"):
    """
    Carrega o DataFrame tratado no MySQL em lote (bulk load).
    """
    if df.empty:
        print("[LOAD] NENHUM dado para carregar.")
        return

    try:
        # Escreve ou apenda os dados no banco relacional
        df.to_sql(
            name=table_name,
            con=engine,
            if_exists='append',
            index=False,
            chunksize=1000
        )
        print(f"[LOAD] Sucesso: {len(df)} registros carregados na tabela '{table_name}'.")
    except Exception as e:
        print(f"[ERRO - LOAD] Falha ao carregar no MySQL: {e}")