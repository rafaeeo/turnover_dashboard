# model.py
import streamlit as st
import pandas as pd
import plotly.express as px
import seaborn as sns
import matplotlib.pyplot as plt
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import classification_report, confusion_matrix

# Constantes
TURNOVER_COL_NAME = "Turnover"
TURNOVER_YES = "Sim"
TURNOVER_NO = "Não"
ID_COL_NAME = "ID"

# Função para treinar e avaliar o modelo
def train_and_evaluate_model(df):
    st.subheader("🤖 Módulo de Análise Preditiva")
    st.markdown("Treinamento de modelo para prever a probabilidade de saída (baseado nos dados filtrados).")
    
    # Preparação dos dados
    df_model = df.copy().dropna()

    # Verifica se há dados suficientes e variação na coluna Turnover
    if df_model.empty or df_model[TURNOVER_COL_NAME].nunique() < 2:
        st.warning("Dados insuficientes ou sem variação na coluna Turnover após filtros/limpeza.")
        return None, None, None
    
    # Mapeamento da coluna de Turnover para valores binários
    df_model["target"] = df_model[TURNOVER_COL_NAME].map({TURNOVER_YES: 1, TURNOVER_NO: 0})
    features_to_drop = [TURNOVER_COL_NAME, "target"]

    ## Adiciona ID_COL_NAME se existir
    if ID_COL_NAME in df_model.columns:
        features_to_drop.append(ID_COL_NAME)
    features_to_drop = [col for col in features_to_drop if col in df_model.columns]
    
    ## Separação de features e target
    X = df_model.drop(columns=features_to_drop)
    y = df_model["target"]

    try:
        X = pd.get_dummies(X, drop_first=True)
    except Exception as e:
        st.error(f"Erro ao aplicar One-Hot Encoding: {e}")
        return None, None, None

    if X.empty:
        st.warning("Nenhuma feature restante após pré-processamento.")
        return None, None, None

    try:
        X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.3, random_state=42, stratify=y)
    except ValueError as e:
        st.warning(f"Erro na separação treino/teste: {e}")
        return None, None, None

    # Treinamento
    with st.spinner("Treinando modelo RandomForest..."):
        model = RandomForestClassifier(random_state=42, class_weight='balanced')
        model.fit(X_train, y_train)
        y_pred = model.predict(X_test)

    st.markdown("### 📊 Resultados do Modelo")
    st.text("Relatório de Classificação:")
    st.text(classification_report(y_test, y_pred, target_names=[TURNOVER_NO, TURNOVER_YES]))

    st.markdown("### 📈 Matriz de Confusão")
    cm = confusion_matrix(y_test, y_pred)
    fig_cm, ax = plt.subplots()
    sns.heatmap(cm, annot=True, fmt='d', cmap='Blues', ax=ax,
                xticklabels=[TURNOVER_NO, TURNOVER_YES], yticklabels=[TURNOVER_NO, TURNOVER_YES])
    ax.set_xlabel("Previsto")
    ax.set_ylabel("Real")
    st.pyplot(fig_cm)

    st.markdown("### 🔍 Importância das Variáveis (Top 15)")
    importances = pd.DataFrame({"Variável": X.columns, "Importância": model.feature_importances_})
    importances = importances.sort_values(by="Importância", ascending=False).head(15)
    fig_imp = px.bar(importances, x="Importância", y="Variável", orientation='h', text_auto='.3f')
    fig_imp.update_layout(yaxis={'categoryorder':'total ascending'})
    st.plotly_chart(fig_imp, use_container_width=True)

    return model, X.columns, df_model
