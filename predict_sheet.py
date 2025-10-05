import pandas as pd
import numpy as np
import joblib

# Definindo caminhos
MODEL_AND_FEATURES_PATH = "data/model_and_features.pkl"
TEST_DATA_PATH = "data/exoplanet_unified.xlsx"
OUTPUT_PATH = "data/exoplanet_unified_teste_results.xlsx"


def prepare_new_data(df, train_features):
    """
    Aplica o mesmo pré-processamento usado no treinamento e 
    garante que as colunas estejam na ordem correta.
    """
    
    # 1. TRATAMENTO DE FLAGS BINÁRIOS (Imputação de 0)
    # Assumimos que a ausência de um flag Kepler significa 0 (False)
    binary_cols = [col for col in train_features if 'fpflag' in col]
    # Certificar que as colunas existem no DF de teste antes de preencher
    for col in binary_cols:
        if col not in df.columns:
            df[col] = pd.NA
    df[binary_cols] = df[binary_cols].fillna(0)
    
    # 2. ONE-HOT ENCODING DA MISSÃO
    df = pd.get_dummies(df, columns=['mission'], drop_first=False)

    # 3. GARANTIR CONSISTÊNCIA DE COLUNAS (CRÍTICO!)
    
    # Preencher colunas One-Hot que podem estar faltando no teste (ex: teste só tem 'TOI')
    ohe_cols = [col for col in train_features if 'mission_' in col]
    for col in ohe_cols:
        if col not in df.columns:
            df[col] = 0

    # 4. IMPUTAÇÃO FINAL E ORDENAÇÃO
    # Preencher todos os NaNs restantes (dos dados originais ou das colunas K2/TOI que faltam) com -999
    df = df.fillna(-999)
    
    # Selecionar e reordenar as colunas EXATAMENTE como no treino
    df_processed = df[train_features]

    return df_processed


# ==== EXECUÇÃO PRINCIPAL DA PREVISÃO ====
if __name__ == "__main__":
    try:
        # 1. CARREGAR MODELO E LISTA DE FEATURES TREINADAS
        # O modelo treinado e a lista de colunas são carregados juntos
        model_data = joblib.load(MODEL_AND_FEATURES_PATH)
        xgb_model = model_data[0]
        train_features = model_data[1]
        
        print(f"Modelo carregado de: {MODEL_AND_FEATURES_PATH}")
        print(f"Modelo espera {len(train_features)} features, na ordem exata.")

        # 2. CARREGAR NOVOS DADOS
        df_new = pd.read_excel(TEST_DATA_PATH)
        
        # Guardar as colunas originais
        df_results = df_new.copy() 

        # 3. PRÉ-PROCESSAR E ORDENAR OS NOVOS DADOS
        X_new = prepare_new_data(df_new, train_features)
        
        # 4. FAZER AS PREVISÕES
        predictions = xgb_model.predict(X_new)
        # Probabilidade de ser 1 (Exoplaneta/Candidato)
        probabilities = xgb_model.predict_proba(X_new)[:, 1] 
        
        # 5. ADICIONAR RESULTADOS
        df_results['prediction_bin'] = predictions.astype(int)
        df_results['probability_exoplanet'] = np.round(probabilities, 4)
        
        # Mapear a previsão binária para texto
        df_results['disposition_predicted'] = df_results['prediction_bin'].map({
            1: 'CANDIDATE/EXOPLANET', 
            0: 'FALSE POSITIVE'
        })
        
        # 6. SALVAR OS RESULTADOS
        df_results.to_excel(OUTPUT_PATH, index=False)
        
        print("\n--- Resultados da Classificação ---")
        print(df_results[['mission', 'disposition_predicted', 'probability_exoplanet']].head())
        print(f"\nClassificação de {len(df_new)} objetos concluída.")
        print(f"Resultados detalhados salvos em: {OUTPUT_PATH}")

    except FileNotFoundError:
        print(f"ERRO: Não foi possível encontrar o arquivo de modelo ({MODEL_AND_FEATURES_PATH}) ou de teste ({TEST_DATA_PATH}).")
    except KeyError as e:
        print(f"ERRO DE COLUNA: Uma feature esperada não foi encontrada ou o nome está incorreto: {e}.")
    except Exception as e:
        print(f"Ocorreu um erro inesperado durante a previsão: {e}")