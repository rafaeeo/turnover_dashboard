# filters.py
import streamlit as st

TURNOVER_COL_NAME = "Turnover"

def apply_filters(df):
    """Aplica filtros da sidebar e retorna o dataframe filtrado."""
    df_filtered = df.copy()
    filtros = {}
    st.sidebar.header("Filtros")

    for col in df_filtered.select_dtypes(include='object').columns:
        if col != TURNOVER_COL_NAME:
            opcoes = df_filtered[col].dropna().unique().tolist()
            if opcoes:
                filtros[col] = st.sidebar.multiselect(f"{col}", opcoes, default=opcoes)
            else:
                filtros[col] = []

    for col, selecionados in filtros.items():
        if selecionados:
            df_filtered = df_filtered[df_filtered[col].isin(selecionados)]

    return df_filtered
