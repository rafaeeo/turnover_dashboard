# data_loader.py
import streamlit as st
import pandas as pd

TURNOVER_COL_NAME = "Turnover"

@st.cache_data
def load_data(uploaded_file):
    """Carrega e pré-processa inicial do dataframe."""
    try:
        df = pd.read_excel(uploaded_file, sheet_name="Base")
        st.sidebar.success("Base carregada com sucesso!")
        st.sidebar.write("Colunas detectadas:", df.columns.tolist())
        return df
    except Exception as e:
        st.sidebar.error(f"Erro ao carregar o arquivo: {e}")
        return None

def find_and_rename_columns(df):
    """Encontra e renomeia colunas chave (Turnover, Gênero, Escolaridade)."""
    df_renamed = df.copy()
    available_cols = df_renamed.columns.tolist()

    potential_turnover_cols = [col for col in available_cols if "deixou" in col.lower() and "empresa" in col.lower()]
    default_turnover_col = potential_turnover_cols[0] if potential_turnover_cols else None
    if not default_turnover_col and TURNOVER_COL_NAME in available_cols:
        default_turnover_col = TURNOVER_COL_NAME

    idx_turnover = available_cols.index(default_turnover_col) if default_turnover_col and default_turnover_col in available_cols else 0

    selected_turnover_col = st.sidebar.selectbox(
        "Confirme a coluna de Turnover:",
        options=available_cols,
        index=idx_turnover,
        key='turnover_selector'
    )

    target_name = TURNOVER_COL_NAME

    if selected_turnover_col != target_name:
        if target_name in df_renamed.columns and target_name != selected_turnover_col:
            st.sidebar.warning(f"A coluna '{target_name}' já existe e é diferente da selecionada ('{selected_turnover_col}'). A coluna '{target_name}' original será removida.")
            df_renamed = df_renamed.drop(columns=[target_name])
        df_renamed = df_renamed.rename(columns={selected_turnover_col: target_name})
        st.sidebar.info(f"Coluna '{selected_turnover_col}' definida como '{target_name}'.")

    potential_gender_cols = [col for col in df_renamed.columns if "genero" in col.lower() or "gênero" in col.lower()]
    col_genero = potential_gender_cols[0] if potential_gender_cols else None

    potential_edu_cols = [col for col in df_renamed.columns if "escolaridade" in col.lower()]
    col_escolaridade = potential_edu_cols[0] if potential_edu_cols else None

    if target_name not in df_renamed.columns:
        st.error(f"Erro Crítico: A coluna '{target_name}' não foi configurada corretamente.")
        st.stop()

    if not df_renamed.columns.is_unique:
        duplicated_cols = df_renamed.columns[df_renamed.columns.duplicated()].tolist()
        st.error(f"Erro Crítico: Colunas duplicadas após renomeação: {duplicated_cols}")
        st.stop()

    return df_renamed, col_genero, col_escolaridade
