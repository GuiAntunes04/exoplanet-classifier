import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.metrics import classification_report, accuracy_score
import xgboost as xgb
import matplotlib.pyplot as plt
import seaborn as sns
import joblib 

# Configuração para evitar warnings e melhorar a visualização no Pandas
pd.set_option('display.max_columns', None)
np.random.seed(42) # Para reprodutibilidade

# 1. CARREGAR E PREPARAR O DATAFRAME
def load_and_prepare_data(path="data/exoplanet_unified.xlsx"):
    """Carrega o dataset unificado e aplica pré-processamento."""
    df = pd.read_excel(path)

    # Lista de colunas a serem EXCLUÍDAS das features (X)
    columns_to_drop = ['label', 'gabarito']
    
    # 1.1. Separar a variável alvo (Label)
    X = df.drop(columns=columns_to_drop, errors='ignore')
    y = df['label'] # Mantém 'label' como a variável Target (Y)

    # 1.2. Codificação Categórica (One-Hot Encoding)
    X = pd.get_dummies(X, columns=['mission'], drop_first=False)
    
    # 1.3. Preencher Colunas Faltantes ('NaN')
    binary_cols = [col for col in X.columns if 'fpflag' in col]
    X[binary_cols] = X[binary_cols].fillna(0)
    
    # Preencher outros NaNs com um valor específico para o XGBoost usar (ex: -999)
    X = X.fillna(-999) 
    
    return X, y

# 2. TREINAR O MODELO XGBOOST
def train_xgboost_model(X, y):
    """Divide os dados e treina o modelo XGBoost."""
    
    # 🛑 INSERIR A DIVISÃO DE DADOS AQUI (CORREÇÃO)
    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.2, stratify=y, random_state=42
    )
    # -----------------------------------------------

    # Definição do Modelo XGBoost (Parâmetros Otimizados)
    model = xgb.XGBClassifier(
        objective='binary:logistic',
        eval_metric='logloss', 
        use_label_encoder=False, 
        
        n_estimators=1500, 
        learning_rate=0.03, 
        max_depth=9,
        
        subsample=0.7, 
        colsample_bytree=0.7, 
        random_state=42,
    )

    print("Iniciando o treinamento do modelo XGBoost...")
    
    # Esta linha agora encontra X_train e y_train
    model.fit(X_train, y_train) 
    
    print("Treinamento concluído.")

    return model, X_test, y_test


# 3. AVALIAR E VISUALIZAR RESULTADOS (Função mantida)
def evaluate_model(model, X_test, y_test):
    """Avalia o modelo e plota a importância das features."""
    
    y_pred = model.predict(X_test)

    # Relatório de Classificação
    print("\n--- Relatório de Classificação ---")
    print(classification_report(y_test, y_pred))
    
    # Importância das Features
    feature_importances = pd.Series(model.feature_importances_, index=X_test.columns)
    feature_importances = feature_importances.sort_values(ascending=False).head(15)

    plt.figure(figsize=(10, 6))
    sns.barplot(x=feature_importances.values, y=feature_importances.index, palette="viridis")
    plt.title('Top 15 Importância das Features (XGBoost)')
    plt.xlabel('Importância (F-Score)')
    plt.ylabel('Feature')
    plt.tight_layout()
    plt.show()

# 4. EXECUÇÃO PRINCIPAL
if __name__ == "__main__":

    # Carregar e Pre-processar
    X, y = load_and_prepare_data()
    
    # Treinar
    xgb_model, X_test, y_test = train_xgboost_model(X, y)
    
    # --- SALVAR MODELO E A ORDEM DAS COLUNAS ---
    model_filename = "data/model_and_features.pkl"
    
    # Salva o modelo treinado (xgb_model) e a lista exata das colunas de treino (X.columns)
    joblib.dump((xgb_model, X.columns.tolist()), model_filename)
    
    print(f"\nModelo XGBoost e lista de features salvas com sucesso em: {model_filename}")
    # --------------------------------------------------------------------------

    # Avaliar
    evaluate_model(xgb_model, X_test, y_test)