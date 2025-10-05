import pandas as pd

# ==== Funções auxiliares ====

# Função Kepler (Padrão de Colunas)
def process_kepler(path):
    df = pd.read_excel(path)

    # Selecionar colunas relevantes...
    cols = [
        "koi_period", "koi_time0bk", "koi_impact", "koi_duration", "koi_depth",
        "koi_prad", "koi_teq", "koi_insol", "koi_model_snr",
        "koi_steff", "koi_slogg", "koi_srad", "ra", "dec", "koi_kepmag",
        "koi_fpflag_nt", "koi_fpflag_ss", "koi_fpflag_co", "koi_fpflag_ec"
    ]
    df = df[cols + ["koi_disposition"]]

    # Lógica que remove CANDIDATEs:
    df["label"] = df["koi_disposition"].apply(
        lambda x: 1 if x == "CONFIRMED" else (0 if x == "FALSE POSITIVE" else None)
    )
    df = df.dropna(subset=["label"])
    
    df["mission"] = "Kepler"

    return df.drop(columns=["koi_disposition"])


# Função TOI (Mapeamento para Kepler)
def process_toi(path):
    df = pd.read_excel(path)

    # Seleção inicial das colunas que serão mapeadas
    cols = [
    "pl_tranmid", "pl_orbper", "pl_trandurh", "pl_trandep", "pl_rade",
    "pl_insol", "pl_eqt", "st_tmag", "st_teff", "st_logg", "st_rad", "ra", "dec"
    ]
    df = df[cols + ["tfopwg_disp"]]

    # Mapeamento de classes para binário
    positive = ["CP", "KP"]
    negative = ["FP", "FA"]

    df["label"] = df["tfopwg_disp"].apply(lambda x: 1 if x in positive else (0 if x in negative else None))

    # Remove classes indefinidas
    df = df.dropna(subset=["label"])

    # 1. MAPEAMENTO DE NOMES (Renomear para o padrão Kepler)
    TOI_MAPPING = {
        "pl_tranmid": "koi_time0bk", "pl_orbper": "koi_period", 
        "pl_trandurh": "koi_duration", "pl_trandep": "koi_depth", 
        "pl_rade": "koi_prad", "pl_insol": "koi_insol", 
        "pl_eqt": "koi_teq", "st_tmag": "koi_kepmag", 
        "st_teff": "koi_steff", "st_logg": "koi_slogg", 
        "st_rad": "koi_srad"
    }
    df = df.rename(columns=TOI_MAPPING)

    # 2. ADIÇÃO DE COLUNAS FALTANTES (Setadas para NaN/0)
    df["koi_impact"] = pd.NA
    df["koi_model_snr"] = pd.NA
    # Flags binários do Kepler não se aplicam ao TOI, use 0 ou False
    df["koi_fpflag_nt"] = 0
    df["koi_fpflag_ss"] = 0 
    df["koi_fpflag_co"] = 0
    df["koi_fpflag_ec"] = 0
    
    df["mission"] = "TOI"

    return df.drop(columns=["tfopwg_disp"])


# Função K2 (Mapeamento para Kepler)
def process_k2(path):
    df = pd.read_excel(path)

    # Seleção inicial de colunas
    cols = [
    # Parâmetros de Trânsito/Planeta (Inferidos)
    "pl_orbper", "pl_orbsmax", "pl_rade", "pl_bmasse", "pl_orbeccen",
    "pl_insol", "pl_eqt",
    # Propriedades Estelares
    "st_teff", "st_rad", "st_mass", "st_logg",
    "ra", "dec"
    ]
    df = df[cols + ["disposition"]]

    positive = ["CONFIRMED"]
    negative = ["FALSE POSITIVE", "REFUTED"]

    df["label"] = df["disposition"].apply(lambda x: 1 if x in positive else (0 if x in negative else None))

    # Remove candidatos indefinidos
    df = df.dropna(subset=["label"])

    # 1. MAPEAMENTO DE NOMES (Renomear para o padrão Kepler)
    K2_MAPPING = {
        "pl_orbper": "koi_period", "pl_rade": "koi_prad",
        "pl_insol": "koi_insol", "pl_eqt": "koi_teq",
        "st_teff": "koi_steff", "st_logg": "koi_slogg",
        "st_rad": "koi_srad",
    }
    df = df.rename(columns=K2_MAPPING)

    # 2. ADIÇÃO DE COLUNAS FALTANTES (Setadas para NaN/0)
    # Duração e Profundidade (Se faltam nos dados K2, adicione NA)
    df["koi_duration"] = pd.NA
    df["koi_depth"] = pd.NA
    df["koi_time0bk"] = pd.NA
    df["koi_impact"] = pd.NA
    df["koi_model_snr"] = pd.NA
    df["koi_kepmag"] = pd.NA # K2 usa outra magnitude, mas preenchemos com NA
    df["koi_fpflag_nt"] = 0
    df["koi_fpflag_ss"] = 0 
    df["koi_fpflag_co"] = 0
    df["koi_fpflag_ec"] = 0

    df["mission"] = "K2"

    return df.drop(columns=["disposition"])


# ==== Execução principal e Unificação ====
if __name__ == "__main__":
    # 1. Processar cada base (Seleção, Labeling e Mapeamento)
    kepler = process_kepler("data/data_kepler.xlsx")
    toi = process_toi("data/data_toi.xlsx")
    k2 = process_k2("data/data_k2.xlsx")

    # 2. Unificar as 3 bases em um único DataFrame
    df_unified = pd.concat([kepler, toi, k2], ignore_index=True)

    # 3. Salvar o arquivo unificado
    df_unified.to_excel("data/exoplanet_unified.xlsx", index=False)
    
    # Salvar tabelas processadas (clean)
    kepler.to_excel("data/kepler_clean.xlsx", index=False)
    toi.to_excel("data/toi_clean.xlsx", index=False)
    k2.to_excel("data/k2_clean.xlsx", index=False)

    print("---")
    print(f"Bases individuais salvas em /data/")
    print(f"Total de observações unificadas: {len(df_unified)}")
    print("DataFrame unificado salvo em data/exoplanet_unified.xlsx, pronto para o XGBoost!")