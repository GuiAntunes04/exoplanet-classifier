import streamlit as st
import pandas as pd
import numpy as np
import joblib

# --- CONFIGURAÇÕES GLOBAIS ---
MODEL_AND_FEATURES_PATH = "data/model_and_features.pkl"
IMPUTATION_VALUE = -999.0
UNCLASSIFIED_MISSION = 'UNCLASSIFIED'

# --- CSS PERSONALIZADO PARA TEMA ESPACIAL ---
def load_custom_css():
    st.markdown("""
    <style>
    /* Tema espacial escuro */
    .stApp {
        background: linear-gradient(135deg, #0a0a0a 0%, #1a1a2e 50%, #16213e 100%);
        color: #ffffff;
    }
    
    /* Efeito de estrelas no fundo */
    .stApp::before {
        content: '';
        position: fixed;
        top: 0;
        left: 0;
        width: 100%;
        height: 100%;
        background-image: 
            radial-gradient(2px 2px at 20px 30px, #eee, transparent),
            radial-gradient(2px 2px at 40px 70px, rgba(255,255,255,0.8), transparent),
            radial-gradient(1px 1px at 90px 40px, #fff, transparent),
            radial-gradient(1px 1px at 130px 80px, rgba(255,255,255,0.6), transparent),
            radial-gradient(2px 2px at 160px 30px, #ddd, transparent);
        background-repeat: repeat;
        background-size: 200px 100px;
        animation: sparkle 20s linear infinite;
        pointer-events: none;
        z-index: -1;
    }
    
    @keyframes sparkle {
        from { transform: translateY(0px); }
        to { transform: translateY(-100px); }
    }
    
    /* Cards para segmentação */
    .parameter-card {
        background: rgba(255, 255, 255, 0.05);
        border: 1px solid rgba(255, 255, 255, 0.1);
        border-radius: 12px;
        padding: 20px;
        margin: 10px 0;
        backdrop-filter: blur(10px);
        box-shadow: 0 8px 32px rgba(0, 0, 0, 0.3);
        transition: all 0.3s ease;
    }
    
    .parameter-card:hover {
        border-color: rgba(255, 255, 255, 0.3);
        box-shadow: 0 12px 40px rgba(0, 0, 0, 0.4);
        transform: translateY(-2px);
    }
    
    /* Título principal */
    .main-title {
        text-align: center;
        font-size: 2.5rem;
        font-weight: bold;
        background: linear-gradient(45deg, #ff6b6b, #4ecdc4, #45b7d1, #96ceb4);
        background-size: 400% 400%;
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        background-clip: text;
        animation: gradientShift 3s ease infinite;
        margin-bottom: 20px;
    }
    
    @keyframes gradientShift {
        0% { background-position: 0% 50%; }
        50% { background-position: 100% 50%; }
        100% { background-position: 0% 50%; }
    }
    
    /* Subtítulos */
    .section-title {
        color: #4ecdc4;
        font-size: 1.5rem;
        font-weight: bold;
        margin: 20px 0 15px 0;
        text-align: center;
        text-shadow: 0 0 10px rgba(78, 205, 196, 0.5);
    }
    
    /* Labels dos parâmetros */
    .param-label {
        color: #ffffff;
        font-weight: bold;
        font-size: 1rem;
        margin-bottom: 8px;
        text-shadow: 0 0 5px rgba(255, 255, 255, 0.3);
    }
    
    /* Inputs personalizados */
    .stNumberInput > div > div > input {
        background: rgba(255, 255, 255, 0.1);
        border: 1px solid rgba(255, 255, 255, 0.2);
        border-radius: 8px;
        color: #ffffff;
        font-size: 1rem;
    }
    
    .stNumberInput > div > div > input:focus {
        border-color: #4ecdc4;
        box-shadow: 0 0 10px rgba(78, 205, 196, 0.3);
    }
    
    /* Checkboxes personalizados */
    .stCheckbox > label {
        color: #ffffff;
        font-weight: 500;
    }
    
    /* Botão principal */
    .stButton > button {
        background: linear-gradient(45deg, #ff6b6b, #4ecdc4);
        color: white;
        border: none;
        border-radius: 25px;
        padding: 12px 30px;
        font-size: 1.2rem;
        font-weight: bold;
        box-shadow: 0 4px 15px rgba(0, 0, 0, 0.3);
        transition: all 0.3s ease;
        width: 100%;
    }
    
    .stButton > button:hover {
        transform: translateY(-2px);
        box-shadow: 0 6px 20px rgba(0, 0, 0, 0.4);
    }
    
    /* Resultado da classificação */
    .result-card {
        background: rgba(255, 255, 255, 0.1);
        border: 2px solid #4ecdc4;
        border-radius: 15px;
        padding: 25px;
        margin: 20px 0;
        text-align: center;
        backdrop-filter: blur(10px);
        box-shadow: 0 10px 30px rgba(78, 205, 196, 0.2);
    }
    
    .result-success {
        border-color: #96ceb4;
        box-shadow: 0 10px 30px rgba(150, 206, 180, 0.3);
    }
    
    .result-error {
        border-color: #ff6b6b;
        box-shadow: 0 10px 30px rgba(255, 107, 107, 0.3);
    }
    
    /* Métricas */
    .stMetric {
        background: rgba(255, 255, 255, 0.05);
        border-radius: 10px;
        padding: 15px;
        border: 1px solid rgba(255, 255, 255, 0.1);
    }
    
    /* Selectbox personalizado */
    .stSelectbox > div > div > select {
        background: rgba(255, 255, 255, 0.1);
        border: 1px solid rgba(255, 255, 255, 0.2);
        border-radius: 8px;
        color: #ffffff;
    }
    
    /* Configuração de classificação */
    .config-section {
        background: rgba(255, 255, 255, 0.05);
        border: 1px solid rgba(255, 255, 255, 0.1);
        border-radius: 12px;
        padding: 20px;
        margin: 20px 0;
        backdrop-filter: blur(10px);
    }
    
    /* Responsividade */
    @media (max-width: 768px) {
        .main-title {
            font-size: 2rem;
        }
        
        .parameter-card {
            padding: 15px;
        }
    }
    
    /* Ocultar elementos padrão do Streamlit */
    .stApp > header {
        background: rgba(0, 0, 0, 0.8);
    }
    
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header {visibility: hidden;}
    
    /* Estilização das Abas */
    .stTabs [data-baseweb="tab-list"] {
        gap: 2px;
        background: rgba(255, 255, 255, 0.05);
        border-radius: 15px;
        padding: 5px;
        backdrop-filter: blur(10px);
        border: 1px solid rgba(255, 255, 255, 0.1);
    }
    
    .stTabs [data-baseweb="tab"] {
        background: transparent;
        border-radius: 12px;
        padding: 12px 24px;
        font-weight: bold;
        font-size: 1.1rem;
        transition: all 0.3s ease;
        border: none;
        color: #888;
        position: relative;
        overflow: hidden;
    }
    
    .stTabs [data-baseweb="tab"]:before {
        content: '';
        position: absolute;
        top: 0;
        left: -100%;
        width: 100%;
        height: 100%;
        background: linear-gradient(90deg, transparent, rgba(255, 255, 255, 0.1), transparent);
        transition: left 0.5s ease;
    }
    
    .stTabs [data-baseweb="tab"]:hover:before {
        left: 100%;
    }
    
    .stTabs [data-baseweb="tab"]:hover {
        background: rgba(78, 205, 196, 0.1);
        color: #4ecdc4;
        transform: translateY(-2px);
        box-shadow: 0 4px 15px rgba(78, 205, 196, 0.2);
    }
    
    .stTabs [aria-selected="true"] {
        background: linear-gradient(45deg, #4ecdc4, #45b7d1);
        color: white;
        box-shadow: 0 4px 20px rgba(78, 205, 196, 0.4);
        transform: translateY(-1px);
    }
    
    .stTabs [aria-selected="true"]:hover {
        background: linear-gradient(45deg, #45b7d1, #4ecdc4);
        transform: translateY(-2px);
        box-shadow: 0 6px 25px rgba(78, 205, 196, 0.5);
    }
    
    /* Ícones das abas */
    .stTabs [data-baseweb="tab"] .stMarkdown {
        display: flex;
        align-items: center;
        gap: 8px;
    }
    
    /* Conteúdo das abas */
    .stTabs [data-baseweb="tab-panel"] {
        background: transparent;
        border-radius: 15px;
        padding: 20px;
        margin-top: 20px;
    }
    
    /* Animação de entrada das abas */
    .stTabs [data-baseweb="tab-panel"] {
        animation: fadeInUp 0.5s ease-out;
    }
    
    @keyframes fadeInUp {
        from {
            opacity: 0;
            transform: translateY(20px);
        }
        to {
            opacity: 1;
            transform: translateY(0);
        }
    }
    
    /* Responsividade das abas */
    @media (max-width: 768px) {
        .stTabs [data-baseweb="tab"] {
            padding: 10px 16px;
            font-size: 1rem;
        }
        
        .stTabs [data-baseweb="tab-list"] {
            flex-direction: column;
            gap: 5px;
        }
    }
    </style>
    """, unsafe_allow_html=True)

# Colunas que serão solicitadas ao usuário
# Formato: (Label para o usuário, Nome da coluna no modelo, Valor Padrão)
COLUMNS_TO_ASK_FOR = [
    ("Período Orbital (dias)", "koi_period", 1.0),
    ("Tempo do 1º Trânsito (BKJD)", "koi_time0bk", 2000.0),
    ("Duração do Trânsito (horas)", "koi_duration", 2.5),
    ("Profundidade (ppm)", "koi_depth", 1000.0),
    ("Raio do Planeta (Rterra)", "koi_prad", 5.0),
    ("Temperatura de Equilíbrio (K)", "koi_teq", 800.0),
    ("Insolação (Ssol)", "koi_insol", 100.0),
    ("Sinal/Ruído (SNR)", "koi_model_snr", 15.0),
    ("Parâmetro de Impacto", "koi_impact", 0.5),
    ("Temperatura Estelar (K)", "koi_steff", 5700.0),
    ("Log g Estelar", "koi_slogg", 4.5),
    ("Raio Estelar (Rsol)", "koi_srad", 1.0),
    ("Magnitude (mag)", "koi_kepmag", 12.0),
    ("Ascensão Reta (graus)", "ra", 290.0),
    ("Declinação (graus)", "dec", 45.0),
    ("Excentricidade Orbital", "pl_orbeccen", 0.0),
    ("Massa do Planeta (Mterra)", "pl_bmasse", 10.0),
    ("Semieixo Maior (AU)", "pl_orbsmax", 0.1),
    ("Massa Estelar (Msol)", "st_mass", 1.0)
]

# --- FUNÇÃO DE PRÉ-PROCESSAMENTO (IDÊNTICA AO TREINO) ---

def prepare_data_for_model(data_dict, train_features):
    """Cria o DataFrame de input e aplica o pré-processamento (IDÊNTICO ao predict_sheet.py)."""
    
    # 1. Cria o DataFrame
    df = pd.DataFrame([data_dict])
    
    # 2. TRATAMENTO DE MISSÃO (apenas se necessário)
    if 'mission' not in df.columns or df['mission'].isna().all():
        df['mission'] = UNCLASSIFIED_MISSION
    
    # 3. TRATAMENTO DE FLAGS BINÁRIOS (Imputação de 0) - IDÊNTICO ao predict_sheet.py
    binary_cols = [col for col in train_features if 'fpflag' in col]
    # Certificar que as colunas existem no DF antes de preencher
    for col in binary_cols:
        if col not in df.columns:
            df[col] = pd.NA
    df[binary_cols] = df[binary_cols].fillna(0)  # Mudança: 0 em vez de 0.0
    
    # 4. ONE-HOT ENCODING DA MISSÃO
    df = pd.get_dummies(df, columns=['mission'], drop_first=False)

    # 5. GARANTIR CONSISTÊNCIA DE COLUNAS (CRÍTICO!) - IDÊNTICO ao predict_sheet.py
    # Preencher colunas One-Hot que podem estar faltando
    ohe_cols = [col for col in train_features if 'mission_' in col]
    for col in ohe_cols:
        if col not in df.columns:
            df[col] = 0  # Mudança: 0 em vez de 0.0
            
    # 6. IMPUTAÇÃO FINAL E ORDENAÇÃO - IDÊNTICO ao predict_sheet.py
    # Preencher todos os NaNs restantes com -999
    df = df.fillna(-999)  # Mudança: -999 em vez de IMPUTATION_VALUE
    
    # Selecionar e reordenar as colunas EXATAMENTE como no treino
    return df[train_features]


# --- CARREGAR MODELO ---
try:
    model_data = joblib.load(MODEL_AND_FEATURES_PATH)
    xgb_model = model_data[0]
    train_features = model_data[1]
except FileNotFoundError:
    st.error(f"Erro: Arquivo do modelo não encontrado em {MODEL_AND_FEATURES_PATH}. Execute o treinamento primeiro!")
    st.stop()


# --- CONFIGURAÇÃO DAS COLUNAS PARA IMPORT ---
REQUIRED_COLUMNS = [
    ("koi_period", "Período Orbital", "Dias", "Trânsito"),
    ("koi_time0bk", "Tempo do 1º Trânsito", "BKJD", "Trânsito"),
    ("koi_impact", "Parâmetro de Impacto", "Normalizado", "Trânsito"),
    ("koi_duration", "Duração do Trânsito", "Horas", "Trânsito"),
    ("koi_depth", "Profundidade do Trânsito", "ppm", "Trânsito"),
    ("koi_prad", "Raio Planetário", "R⊕", "Planeta"),
    ("koi_teq", "Temperatura de Equilíbrio", "K", "Planeta"),
    ("koi_insol", "Insolação", "S⊕", "Planeta"),
    ("koi_model_snr", "Razão Sinal/Ruído", "Unidade (s/ dimensão)", "Qualidade"),
    ("koi_steff", "Temperatura Estelar", "K", "Estrela"),
    ("koi_slogg", "Log g Estelar", "Log₁₀ (cgs)", "Estrela"),
    ("koi_srad", "Raio Estelar", "R☉", "Estrela"),
    ("ra", "Ascensão Reta", "Graus", "Coordenada"),
    ("dec", "Declinação", "Graus", "Coordenada"),
    ("koi_kepmag", "Magnitude Kepler", "mag", "Estrela"),
    ("koi_fpflag_nt", "Flag: Não-Trânsito", "0 ou 1", "Flag FP"),
    ("koi_fpflag_ss", "Flag: Eclipse Secundário", "0 ou 1", "Flag FP"),
    ("koi_fpflag_co", "Flag: Desvio Centroide", "0 ou 1", "Flag FP"),
    ("koi_fpflag_ec", "Flag: Contaminação", "0 ou 1", "Flag FP"),
    ("mission", "Contexto da Missão", "Texto", "Missão"),
    ("pl_orbsmax", "Semieixo Maior", "AU", "Órbita Extra"),
    ("pl_bmasse", "Massa Planetária", "M⊕", "Massa Extra"),
    ("pl_orbeccen", "Excentricidade Orbital", "(Valor de 0 a 1)", "Órbita Extra"),
    ("st_mass", "Massa Estelar", "M☉", "Massa Estelar Extra")
]

# --- INTERFACE STREAMLIT ---

st.set_page_config(
    page_title="Classificador de Exoplanetas", 
    layout="wide",
    initial_sidebar_state="collapsed"
)

# Carregar CSS personalizado
load_custom_css()

# Título principal com estilo personalizado
st.markdown("""
<div class="main-title">
    🪐 Classificador de Exoplanetas (Modelo XGBoost)
</div>
""", unsafe_allow_html=True)

# Sistema de abas
tab1, tab2 = st.tabs(["🔬 Classificação Individual", "📊 Importação em Lote"])

with tab1:
    st.markdown("""
    <div style="text-align: center; color: #cccccc; margin-bottom: 30px; font-size: 1.1rem;">
        Use as caixas de seleção ao lado de cada campo. <strong>Desmarque a caixa</strong> se o valor for desconhecido (será tratado como NaN).
    </div>
    """, unsafe_allow_html=True)

with tab1:
    # Armazenará os dados de entrada
    input_data = {}

    # Seção de Parâmetros Astronômicos
    st.markdown('<div class="section-title">🌟 Parâmetros Astronômicos</div>', unsafe_allow_html=True)

    # Layout em 3 colunas
    cols_input = st.columns(3)

    # 1. ENTRADAS PARA PARÂMETROS NUMÉRICOS
    for i, (prompt, col_name, default_value) in enumerate(COLUMNS_TO_ASK_FOR):
        col = cols_input[i % 3] # Distribui as entradas nas colunas

        with col:
            # Card personalizado para cada parâmetro
            st.markdown(f"""
            <div class="parameter-card">
                <div class="param-label">{prompt}</div>
            </div>
            """, unsafe_allow_html=True)
            
            # Checkbox para determinar se o valor é conhecido (True) ou NaN (False)
            is_known = st.checkbox(
                f"Valor Conhecido", 
                value=True, # Por padrão, esperamos que o usuário insira o valor
                key=f'check_{col_name}'
            )
            
            if is_known:
                # Se a caixa estiver marcada, exibe o campo de entrada
                user_value = st.number_input(
                    label=' ', # Label vazio para economizar espaço
                    value=default_value,
                    format="%.6f",
                    key=col_name
                )
                input_data[col_name] = user_value
            else:
                # Se a caixa estiver desmarcada, o valor é NaN
                input_data[col_name] = np.nan
                st.markdown("""
                <div style="text-align: center; color: #ff6b6b; font-style: italic; padding: 10px;">
                    — Valor Omitido (NaN) —
                </div>
                """, unsafe_allow_html=True)


    # 2. ENTRADAS PARA MISSÃO E FLAGS (Abaixo das colunas)
    st.markdown('<div class="section-title">⚙️ Configuração de Classificação</div>', unsafe_allow_html=True)

    # Card para configuração
    st.markdown('<div class="config-section">', unsafe_allow_html=True)

    col_m, col_f1, col_f2, col_f3, col_f4 = st.columns(5)

    # Missão (Dropdown)
    with col_m:
        st.markdown("**Missão Original**")
        input_data['mission'] = st.selectbox(
            "Selecione a missão",
            options=['Kepler', 'TOI', 'K2', 'NO-MISSION'],
            index=3, # Padrão para 'NO-MISSION' (que será UNCLASSIFIED)
            label_visibility="collapsed"
        )

    # Flags de Falso Positivo (Checkboxes)
    with col_f1:
        st.markdown("**FP: Não Trânsito**")
        input_data['koi_fpflag_nt'] = 1.0 if st.checkbox("É um ruído?", value=False, label_visibility="collapsed") else 0.0

    with col_f2:
        st.markdown("**FP: Eclipse Secundário**")
        input_data['koi_fpflag_ss'] = 1.0 if st.checkbox("Indica estrela binária?", value=False, label_visibility="collapsed") else 0.0

    with col_f3:
        st.markdown("**FP: Desvio Centroide**")
        input_data['koi_fpflag_co'] = 1.0 if st.checkbox("Indica contaminação?", value=False, label_visibility="collapsed") else 0.0

    with col_f4:
        st.markdown("**FP: Contaminação**")
        input_data['koi_fpflag_ec'] = 1.0 if st.checkbox("Sinal compartilhado?", value=False, label_visibility="collapsed") else 0.0

    st.markdown('</div>', unsafe_allow_html=True)


    # 3. Lógica de Previsão
    st.markdown('<div style="text-align: center; margin: 30px 0;">', unsafe_allow_html=True)
    if st.button("🚀 Classificar Objeto", type="primary"):
        st.markdown('</div>', unsafe_allow_html=True)
        
        # 🛑 CRÍTICO: Ajustar o valor da missão antes de enviar ao pré-processamento
        # Isso garante que 'NO-MISSION' se torne 'UNCLASSIFIED' se necessário
        if input_data['mission'] == 'NO-MISSION':
            input_data['mission'] = UNCLASSIFIED_MISSION
            
        # Aplica o pré-processamento
        X_processed = prepare_data_for_model(input_data, train_features)
        
        # Realiza a Previsão
        predictions = xgb_model.predict(X_processed)
        probabilities = xgb_model.predict_proba(X_processed)[0]
        
        prob_exoplanet = probabilities[1]
        
        # Seção de resultados com estilo personalizado
        st.markdown('<div class="section-title">🎯 Resultado da Classificação</div>', unsafe_allow_html=True)
        
        # Card de resultado personalizado
        result_class = "result-success" if prob_exoplanet > 0.5 else "result-error"
        result_text = "CANDIDATE/EXOPLANETA (Classe 1)" if prob_exoplanet > 0.5 else "FALSO POSITIVO (Classe 0)"
        result_icon = "🪐" if prob_exoplanet > 0.5 else "❌"
        
        st.markdown(f"""
        <div class="result-card {result_class}">
            <h2 style="margin: 0 0 15px 0; font-size: 1.8rem;">
                {result_icon} DISPOSIÇÃO PREVISTA: {result_text}
            </h2>
            <div style="font-size: 3rem; font-weight: bold; margin: 20px 0; color: #4ecdc4;">
                {prob_exoplanet * 100:.2f}%
            </div>
            <p style="margin: 0; font-size: 1.1rem; color: #cccccc;">
                Probabilidade de ser Exoplaneta
            </p>
        </div>
        """, unsafe_allow_html=True)
        
        # Informação adicional
        st.markdown("""
        <div style="text-align: center; color: #888; font-style: italic; margin-top: 20px;">
            Previsão baseada no seu modelo XGBoost treinado
        </div>
        """, unsafe_allow_html=True)
    else:
        st.markdown('</div>', unsafe_allow_html=True)

with tab2:
    st.markdown("""
    <div style="text-align: center; color: #cccccc; margin-bottom: 30px; font-size: 1.1rem;">
        Importe uma planilha Excel ou CSV para classificar múltiplos objetos de uma vez.
    </div>
    """, unsafe_allow_html=True)
    
    # Seção de instruções
    st.markdown('<div class="section-title">📋 Instruções para Importação</div>', unsafe_allow_html=True)
    
    # Renderiza o texto e a lista de regras normalmente
    st.markdown("""
    <div class="config-section">
        <h4 style="color: #4ecdc4; margin-bottom: 15px;">📝 Formato da Planilha</h4>
        <p style="color: #cccccc; margin-bottom: 10px;">
            Sua planilha deve conter exatamente <strong>24 colunas</strong> na ordem especificada abaixo:
        </p>
        <ul style="color: #cccccc; margin-left: 20px;">
            <li>Formato aceito: <strong>Excel (.xlsx, .xls)</strong> ou <strong>CSV (.csv)</strong></li>
            <li>Primeira linha deve conter os nomes das colunas</li>
            <li>Valores ausentes devem ser deixados em branco ou como NaN</li>
            <li>Flags FP devem ser 0 ou 1</li>
            <li>Unidades devem estar conforme especificado na tabela</li>
        </ul>
    </div>
    """, unsafe_allow_html=True)
    
    # Botão para baixar planilha de exemplo
    st.markdown('<div class="section-title">📥 Planilha de Exemplo</div>', unsafe_allow_html=True)
    
    # Carregar e disponibilizar a planilha de exemplo
    try:
        with open("example_exoplanet_spreadsheet.csv", "r", encoding="utf-8") as f:
            csv_data = f.read()
        
        st.markdown("""
        <div class="config-section">
            <h4 style="color: #4ecdc4; margin-bottom: 15px;">📋 Baixe o Template</h4>
            <p style="color: #cccccc; margin-bottom: 15px;">
                Use esta planilha de exemplo como template para criar seus próprios dados. 
                Ela contém 3 exemplos com diferentes missões (Kepler, TOI, K2) e todas as colunas na ordem correta.
            </p>
        </div>
        """, unsafe_allow_html=True)
        
        # CSS específico para o botão de download
        st.markdown("""
        <style>
        /* Forçar estilo para todos os botões de download */
        .stDownloadButton > button,
        .stDownloadButton > button:focus,
        .stDownloadButton > button:active,
        .stDownloadButton > button:visited {
            background: linear-gradient(45deg, #4ecdc4, #45b7d1) !important;
            background-color: #4ecdc4 !important;
            color: white !important;
            border: none !important;
            border-radius: 25px !important;
            padding: 12px 30px !important;
            font-size: 1.1rem !important;
            font-weight: bold !important;
            box-shadow: 0 4px 15px rgba(0, 0, 0, 0.3) !important;
            transition: all 0.3s ease !important;
            width: 100% !important;
            text-align: center !important;
            cursor: pointer !important;
        }
        
        .stDownloadButton > button:hover {
            background: linear-gradient(45deg, #45b7d1, #4ecdc4) !important;
            background-color: #45b7d1 !important;
            transform: translateY(-2px) !important;
            box-shadow: 0 6px 20px rgba(0, 0, 0, 0.4) !important;
            color: white !important;
        }
        
        /* Garantir que o texto seja sempre visível */
        .stDownloadButton > button * {
            color: white !important;
        }
        
        /* Estilo específico para o botão de exemplo */
        div[data-testid="stDownloadButton"] > button {
            background: linear-gradient(45deg, #4ecdc4, #45b7d1) !important;
            background-color: #4ecdc4 !important;
            color: white !important;
        }
        </style>
        """, unsafe_allow_html=True)
        
        # Botão de download único e bem estilizado
        st.markdown("""
        <div style="text-align: center; margin: 20px 0;">
            <a href="data:text/csv;charset=utf-8,""" + csv_data.replace('\n', '%0A') + """" 
               download="example_exoplanet_spreadsheet.csv" 
               style="display: inline-block; background: linear-gradient(45deg, #4ecdc4, #45b7d1); 
                      color: white; padding: 15px 40px; border-radius: 25px; 
                      text-decoration: none; font-weight: bold; font-size: 1.2rem;
                      box-shadow: 0 4px 15px rgba(0, 0, 0, 0.3); transition: all 0.3s ease;
                      border: none; cursor: pointer;"
               onmouseover="this.style.transform='translateY(-2px)'; this.style.boxShadow='0 6px 20px rgba(0, 0, 0, 0.4)'; this.style.background='linear-gradient(45deg, #45b7d1, #4ecdc4)'"
               onmouseout="this.style.transform='translateY(0)'; this.style.boxShadow='0 4px 15px rgba(0, 0, 0, 0.3)'; this.style.background='linear-gradient(45deg, #4ecdc4, #45b7d1)'">
                📥 Baixar Planilha de Exemplo (CSV)
            </a>
        </div>
        """, unsafe_allow_html=True)
        
        # Mostrar preview da planilha de exemplo
        st.markdown("""
        <div style="margin-top: 20px;">
            <h4 style="color: #4ecdc4; margin-bottom: 15px;">👀 Preview da Planilha de Exemplo</h4>
        </div>
        """, unsafe_allow_html=True)
        
        # Carregar e exibir preview
        df_example = pd.read_csv("example_exoplanet_spreadsheet.csv")
        st.dataframe(df_example, use_container_width=True, hide_index=True)
        
    except FileNotFoundError:
        st.error("❌ Arquivo de exemplo não encontrado. Verifique se 'example_exoplanet_spreadsheet.csv' existe no diretório.")
    except Exception as e:
        st.error(f"❌ Erro ao carregar planilha de exemplo: {str(e)}") 

    # --- Renderização SEPARADA do bloco problemático ---
    st.markdown('''
<h4 style="color: #4ecdc4; margin: 20px 0 15px 0;">🔬 Símbolos e Unidades</h4>
<div style="display: grid; grid-template-columns: repeat(auto-fit, minmax(200px, 1fr)); gap: 10px; color: #cccccc;">
    <div><strong>R⊕</strong> = Raio da Terra</div>
    <div><strong>M⊕</strong> = Massa da Terra</div>
    <div><strong>R☉</strong> = Raio Solar</div>
    <div><strong>M☉</strong> = Massa Solar</div>
    <div><strong>S⊕</strong> = Insolação da Terra</div>
    <div><strong>BKJD</strong> = Barycentric Kepler Julian Date</div>
    <div><strong>AU</strong> = Unidade Astronômica</div>
    <div><strong>ppm</strong> = Partes por milhão</div>
</div>
''', unsafe_allow_html=True)
    
    # Tabela com a ordem das colunas
    st.markdown('<div class="section-title">📊 Ordem das Colunas</div>', unsafe_allow_html=True)
    
    # Criar DataFrame para exibir a tabela
    columns_df = pd.DataFrame({
        '#': range(1, len(REQUIRED_COLUMNS) + 1),
        'Nome Técnico': [col[0] for col in REQUIRED_COLUMNS],
        'Conceito': [col[1] for col in REQUIRED_COLUMNS],
        'Unidade': [col[2] for col in REQUIRED_COLUMNS],
        'Categoria': [col[3] for col in REQUIRED_COLUMNS]
    })
    
    # Exibir tabela com estilo
    st.markdown("""
    <div class="config-section">
    """, unsafe_allow_html=True)
    
    st.dataframe(
        columns_df,
        use_container_width=True,
        hide_index=True,
        height=700
    )
    
    st.markdown("</div>", unsafe_allow_html=True)
    
    # Upload de arquivo
    st.markdown('<div class="section-title">📁 Upload da Planilha</div>', unsafe_allow_html=True)
    
    uploaded_file = st.file_uploader(
        "Escolha um arquivo Excel ou CSV",
        type=['xlsx', 'xls', 'csv'],
        help="Arquivo deve conter as 24 colunas na ordem especificada"
    )
    
    if uploaded_file is not None:
        try:
            # Ler o arquivo
            if uploaded_file.name.endswith('.csv'):
                df = pd.read_csv(uploaded_file)
            else:
                df = pd.read_excel(uploaded_file)
            
            st.success(f"✅ Arquivo carregado com sucesso! {len(df)} registros encontrados.")
            
            # Validar colunas
            required_col_names = [col[0] for col in REQUIRED_COLUMNS]
            missing_cols = [col for col in required_col_names if col not in df.columns]
            extra_cols = [col for col in df.columns if col not in required_col_names]
            
            if missing_cols:
                st.error(f"❌ Colunas ausentes: {', '.join(missing_cols)}")
            if extra_cols:
                st.warning(f"⚠️ Colunas extras (serão ignoradas): {', '.join(extra_cols)}")
            
            # Verificar ordem das colunas
            df_cols = list(df.columns)
            correct_order = [col for col in required_col_names if col in df_cols]
            wrong_order = []
            
            for i, col in enumerate(correct_order):
                if df_cols[i] != col:
                    wrong_order.append(f"Posição {i+1}: esperado '{col}', encontrado '{df_cols[i]}'")
            
            if wrong_order:
                st.warning("⚠️ Ordem das colunas incorreta:")
                for error in wrong_order:
                    st.write(f"  • {error}")
            else:
                st.success("✅ Ordem das colunas está correta!")
            
            # Mostrar preview dos dados
            st.markdown('<div class="section-title">👀 Preview dos Dados</div>', unsafe_allow_html=True)
            st.dataframe(df.head(10), use_container_width=True)
            
            # Botão para processar
            if not missing_cols and not wrong_order:
                st.markdown('<div style="text-align: center; margin: 30px 0;">', unsafe_allow_html=True)
                if st.button("🚀 Processar Planilha", type="primary"):
                    st.markdown('</div>', unsafe_allow_html=True)
                    
                    # Processar cada linha
                    results = []
                    progress_bar = st.progress(0)
                    status_text = st.empty()
                    
                    for idx, row in df.iterrows():
                        status_text.text(f'Processando registro {idx + 1} de {len(df)}...')
                        
                        # Converter linha para dicionário
                        row_data = row.to_dict()
                        
                        # Ajustar missão se necessário
                        if row_data.get('mission') == 'NO-MISSION' or pd.isna(row_data.get('mission')):
                            row_data['mission'] = UNCLASSIFIED_MISSION
                        
                        # Aplicar pré-processamento
                        X_processed = prepare_data_for_model(row_data, train_features)
                        
                        # Realizar previsão
                        predictions = xgb_model.predict(X_processed)
                        probabilities = xgb_model.predict_proba(X_processed)[0]
                        
                        prob_exoplanet = probabilities[1]
                        prediction_class = "EXOPLANETA" if prob_exoplanet > 0.5 else "FALSO_POSITIVO"
                        
                        results.append({
                            'Registro': idx + 1,
                            'Predição': prediction_class,
                            'Probabilidade_Exoplaneta': f"{prob_exoplanet * 100:.2f}%",
                            'Probabilidade_Numerica': prob_exoplanet
                        })
                        
                        progress_bar.progress((idx + 1) / len(df))
                    
                    status_text.text('Processamento concluído!')
                    
                    # Exibir resultados
                    st.markdown('<div class="section-title">🎯 Resultados da Classificação</div>', unsafe_allow_html=True)
                    
                    results_df = pd.DataFrame(results)
                    
                    # Estatísticas gerais
                    exoplanet_count = len([r for r in results if r['Predição'] == 'EXOPLANETA'])
                    fp_count = len([r for r in results if r['Predição'] == 'FALSO_POSITIVO'])
                    
                    col1, col2, col3 = st.columns(3)
                    with col1:
                        st.metric("Total de Registros", len(results))
                    with col2:
                        st.metric("Exoplanetas Detectados", exoplanet_count)
                    with col3:
                        st.metric("Falsos Positivos", fp_count)
                    
                    # Tabela de resultados
                    st.dataframe(
                        results_df[['Registro', 'Predição', 'Probabilidade_Exoplaneta']],
                        use_container_width=True,
                        hide_index=True
                    )
                    
                    # Download dos resultados
                    csv_results = results_df.to_csv(index=False)
                    st.download_button(
                        label="📥 Baixar Resultados (CSV)",
                        data=csv_results,
                        file_name=f"resultados_classificacao_{len(results)}_registros.csv",
                        mime="text/csv",
                        key="download_results_csv"
                    )
                    
            else:
                st.markdown('</div>', unsafe_allow_html=True)
                st.error("❌ Corrija os problemas acima antes de processar a planilha.")
        
        except Exception as e:
            st.error(f"❌ Erro ao processar o arquivo: {str(e)}")
            st.write("Verifique se o arquivo está no formato correto e tente novamente.")