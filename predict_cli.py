import pandas as pd
import numpy as np
import joblib
import sys

# --- Configurações ---
MODEL_AND_FEATURES_PATH = "data/model_and_features.pkl"
IMPUTATION_VALUE = -999.0
UNCLASSIFIED_MISSION = 'UNCLASSIFIED'
COLUMNS_TO_ASK_FOR = [
    # DADOS DE TRÂNSITO E PLANETA
    ("Período Orbital (dias)", "koi_period", float),
    ("Tempo do 1º Trânsito (BKJD)", "koi_time0bk", float),
    ("Duração do Trânsito (horas)", "koi_duration", float),
    ("Profundidade do Trânsito (ppm)", "koi_depth", float),
    ("Raio do Planeta (Rterra)", "koi_prad", float),
    ("Temperatura de Equilíbrio (K)", "koi_teq", float),
    ("Insolação (Ssol)", "koi_insol", float),
    ("Sinal/Ruído (SNR)", "koi_model_snr", float),
    ("Parâmetro de Impacto", "koi_impact", float),

    # PROPRIEDADES ESTELARES
    ("Temperatura Estelar (K)", "koi_steff", float),
    ("Log g Estelar", "koi_slogg", float),
    ("Raio Estelar (Rsol)", "koi_srad", float),
    ("Magnitude Kepler (mag)", "koi_kepmag", float),
    
    # COORDENADAS (Opcional)
    ("Ascensão Reta (graus)", "ra", float),
    ("Declinação (graus)", "dec", float),

    # EXTRAS DO K2/ARQUIVO (Opcional)
    ("Excentricidade Orbital", "pl_orbeccen", float),
    ("Massa do Planeta (Mterra)", "pl_bmasse", float),
    ("Semieixo Maior (AU)", "pl_orbsmax", float),
    ("Massa Estelar (Msol)", "st_mass", float)
]


def get_user_input():
    """Coleta os dados do novo objeto de forma interativa."""
    data = {}
    print("\n--- INSERÇÃO DE DADOS DO NOVO OBJETO ---")
    print("Pressione ENTER sem valor para pular (tratar como ausente/NaN).\n")

    # 1. Coletar features numéricas
    for prompt, col_name, data_type in COLUMNS_TO_ASK_FOR:
        while True:
            try:
                user_input = input(f"-> {prompt} [Enter para pular]: ")
                
                if user_input == "":
                    data[col_name] = np.nan # Usa NaN se o usuário pular
                    break
                
                data[col_name] = data_type(user_input)
                break
            except ValueError:
                print("Valor inválido. Insira apenas números.")
    
    # 2. Coletar Missão (Obrigatória para o OHE, mas preenchida se vazia)
    mission = input("\n-> Missão (Ex: Kepler, TOI, K2) [Opcional]: ")
    data['mission'] = mission if mission else np.nan # Usa NaN se vazio

    # 3. Coletar Flags de Falso Positivo (Geralmente 0/1)
    # Para simplicidade, vamos assumir 0 para flags se não informados
    print("\n--- FLAGS DE FALSO POSITIVO (0=Não, 1=Sim) ---")
    for flag_name in ['koi_fpflag_nt', 'koi_fpflag_ss', 'koi_fpflag_co', 'koi_fpflag_ec']:
        while True:
            try:
                val = input(f"-> {flag_name} (0 ou 1) [Enter para 0]: ")
                data[flag_name] = int(val) if val else 0
                break
            except ValueError:
                print("Valor inválido. Insira apenas 0 ou 1.")

    return pd.DataFrame([data])


def prepare_for_prediction(df_new, train_features):
    """Aplica o pré-processamento final (OHE e Imputação) para o modelo."""
    
    # 1. TRATAR MISSÃO AUSENTE
    if 'mission' not in df_new.columns:
        df_new['mission'] = UNCLASSIFIED_MISSION
    else:
        # Preenche qualquer NaN na coluna 'mission' com 'UNCLASSIFIED'
        df_new['mission'] = df_new['mission'].fillna(UNCLASSIFIED_MISSION)
    
    # 2. ONE-HOT ENCODING
    df_new = pd.get_dummies(df_new, columns=['mission'], drop_first=False)

    # 3. GARANTIR CONSISTÊNCIA DE COLUNAS (CRÍTICO!)
    # Cria colunas OHE ausentes e preenche com 0
    ohe_cols = [col for col in train_features if 'mission_' in col]
    for col in ohe_cols:
        if col not in df_new.columns:
            df_new[col] = 0.0

    # 4. IMPUTAÇÃO DE NaNs com -999 (para features numéricas restantes)
    df_new = df_new.fillna(IMPUTATION_VALUE)
    
    # 5. ORDENAÇÃO FINAL
    # Garante que as colunas estejam na ordem exata do treinamento
    try:
        df_processed = df_new[train_features]
    except KeyError as e:
        print(f"\n[ERRO FATAL] A feature {e} está faltando no seu input final.")
        print("Verifique se inseriu todos os dados necessários ou se os nomes das colunas coincidem.")
        sys.exit(1)
    
    return df_processed


# ==== EXECUÇÃO PRINCIPAL ====
if __name__ == "__main__":
    try:
        # 1. CARREGAR MODELO E LISTA DE FEATURES TREINADAS
        model_data = joblib.load(MODEL_AND_FEATURES_PATH)
        xgb_model = model_data[0]
        train_features = model_data[1]
        
        print(f"\n[MODELO] XGBoost carregado. Pronto para predição.")

        # 2. COLETAR NOVOS DADOS
        df_new_input = get_user_input()
        
        # 3. PRÉ-PROCESSAR E ORDENAR
        X_new_processed = prepare_for_prediction(df_new_input, train_features)
        
        # 4. FAZER A PREVISÃO
        proba = xgb_model.predict_proba(X_new_processed)[0] # Retorna array [P(0), P(1)]
        
        # Resultado Final
        prob_exoplanet = proba[1]
        result_class = "EXOPLANETA/CANDIDATO" if prob_exoplanet > 0.5 else "FALSO POSITIVO"
        
        print("\n" + "="*50)
        print(f"| CLASSIFICAÇÃO FINAL: {result_class:<28}|")
        print(f"| PROBABILIDADE de ser EXOPLANETA: {prob_exoplanet * 100:.2f}%  |")
        print("="*50)

    except FileNotFoundError:
        print(f"\n[ERRO] Arquivo do modelo não encontrado: {MODEL_AND_FEATURES_PATH}")
        print("Certifique-se de que o treinamento foi executado e o arquivo .pkl foi salvo corretamente.")
    except Exception as e:
        print(f"\n[ERRO INESPERADO] Falha ao executar o script: {e}")