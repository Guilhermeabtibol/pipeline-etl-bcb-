import pandas as pd

def transform_economic_data(df: pd.DataFrame, indicador_nome: str) -> pd.DataFrame:
    """
    Aplica tratamento de dados, conversões de tipos e cálculos analíticos.
    """
    if df.empty:
        print("[TRANSFORM] DataFrame vazio fornecido para transformação.")
        return df

    # 1. Renomear colunas originais da API
    df = df.rename(columns={'data': 'data_registro', 'valor': 'valor_indicador'})

    # 2. Tipagem adequada dos dados
    df['data_registro'] = pd.to_datetime(df['data_registro'], format='%d/%m/%Y')
    df['valor_indicador'] = pd.to_numeric(df['valor_indicador'], errors='coerce')

    # 3. Remover registros nulos ou inválidos
    df = df.dropna(subset=['valor_indicador'])

    # 4. Enriquecimento dos dados
    df['indicador'] = indicador_nome
    df['ano'] = df['data_registro'].dt.year
    df['mes'] = df['data_registro'].dt.month
    df['dia_semana'] = df['data_registro'].dt.day_name()
    
    # Média móvel de 7 períodos arredondada para 4 casas decimais
    df['media_movel_7d'] = df['valor_indicador'].rolling(window=7, min_periods=1).mean().round(4)

    # Reordenar colunas
    cols = ['data_registro', 'indicador', 'valor_indicador', 'media_movel_7d', 'ano', 'mes', 'dia_semana']
    
    print(f"[TRANSFORM] Dados transformados e limpos com sucesso ({len(df)} linhas).")
    return df[cols]