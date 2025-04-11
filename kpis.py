# kpis.py
import streamlit as st

TURNOVER_COL_NAME = "Turnover"
TURNOVER_YES = "Sim"


def display_kpis(df):
    """Calcula e exibe os KPIs principais do dashboard."""
    total = df.shape[0]
    saiu = (df[TURNOVER_COL_NAME] == TURNOVER_YES).sum()
    taxa = saiu / total * 100 if total > 0 else 0

    st.subheader("🔍 Visão Geral")
    col1, col2, col3 = st.columns(3)
    col1.metric("Total de Funcionários (Filtrado)", total)
    col2.metric("Turnover Absoluto (Filtrado)", saiu)
    col3.metric("Taxa de Turnover (%) (Filtrada)", f"{taxa:.1f}%")
