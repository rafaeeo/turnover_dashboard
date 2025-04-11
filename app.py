# app.py
import streamlit as st
from data_loader import load_data, find_and_rename_columns
from filters import apply_filters
from kpis import display_kpis
from visualizations import plot_exploratory_analysis, plot_correlation_heatmap
from model_utils import train_and_evaluate_model
from simulator import run_simulation

st.set_page_config(page_title="Painel de Turnover", layout="wide")
st.title("📊 Dashboard de Turnover - RH")

uploaded_file = st.sidebar.file_uploader("Faça upload do arquivo Excel da base de RH:", type=["xlsx"])

if uploaded_file:
    df_original = load_data(uploaded_file)

    if df_original is not None:
        df_processed, col_genero, col_escolaridade = find_and_rename_columns(df_original)

        if not df_processed.index.is_unique:
            st.warning("Detectado índice duplicado após carregamento. Resetando índice.")
            df_processed = df_processed.reset_index(drop=True)

        df_filtered = apply_filters(df_processed)

        if df_filtered.empty:
            st.warning("Nenhum dado corresponde aos filtros selecionados.")
        else:
            if not df_filtered.index.is_unique:
                st.warning("Detectado índice duplicado após filtragem. Resetando índice.")
                df_filtered = df_filtered.reset_index(drop=True)

            display_kpis(df_filtered)

            tab_explore, tab_corr, tab_predict, tab_sim = st.tabs([
                "Análise Exploratória", "Correlação", "Modelo Preditivo", "Simulador"])

            with tab_explore:
                plot_exploratory_analysis(df_filtered, col_genero, col_escolaridade)

            with tab_corr:
                plot_correlation_heatmap(df_filtered)

            with tab_predict:
                model, train_cols, df_model_used = train_and_evaluate_model(df_filtered)

            with tab_sim:
                run_simulation(model, train_cols, df_model_used)
else:
    st.info("Por favor, envie a base de dados no formato Excel (.xlsx) para iniciar a análise.")
