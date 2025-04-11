# visualizations.py
import streamlit as st
import plotly.express as px
import seaborn as sns
import matplotlib.pyplot as plt
import numpy as np

TURNOVER_COL_NAME = "Turnover"
TURNOVER_YES = "Sim"
ID_COL_NAME = "ID"


def plot_exploratory_analysis(df, col_genero, col_escolaridade):
    st.subheader("📊 Análise Exploratória (Dados Filtrados)")

    colunas_cat = [col for col in df.select_dtypes(include='object').columns if col not in [TURNOVER_COL_NAME, ID_COL_NAME]]
    colunas_num = [col for col in df.select_dtypes(include='number').columns if col != ID_COL_NAME]

    st.markdown("#### 🎯 Distribuição Categórica por Turnover")
    tabs_cat = st.tabs([col for col in colunas_cat if df[col].nunique() <= 15])
    cat_cols_to_plot = [col for col in colunas_cat if df[col].nunique() <= 15]

    for i, col in enumerate(cat_cols_to_plot):
        with tabs_cat[i]:
            try:
                fig = px.histogram(df, x=col, color=TURNOVER_COL_NAME, barmode='group', text_auto=True)
                fig.update_layout(yaxis_title="Contagem")
                st.plotly_chart(fig, use_container_width=True)
            except Exception as e:
                st.warning(f"Não foi possível gerar o gráfico para {col}: {e}")

    high_cardinality_cols = [col for col in colunas_cat if df[col].nunique() > 15]
    if high_cardinality_cols:
        st.info(f"Variáveis com muitas categorias (>15) não plotadas: {', '.join(high_cardinality_cols)}")

    st.markdown(f"#### 📈 Variáveis Numéricas vs Turnover")
    tabs_num_mean = st.tabs([f"Média de {col}" for col in colunas_num])
    for i, col in enumerate(colunas_num):
        with tabs_num_mean[i]:
            group = df.groupby(TURNOVER_COL_NAME)[col].mean().reset_index()
            fig = px.bar(group, x=TURNOVER_COL_NAME, y=col, text_auto=".2f")
            st.plotly_chart(fig, use_container_width=True, key=f"bar_mean_{col}")

    st.markdown(f"#### 🎻 Distribuição Numérica por Turnover")
    tabs_num_dist = st.tabs([f"Distribuição de {col}" for col in colunas_num])
    for i, col in enumerate(colunas_num):
        with tabs_num_dist[i]:
            fig = px.box(df, x=TURNOVER_COL_NAME, y=col, color=TURNOVER_COL_NAME)
            st.plotly_chart(fig, use_container_width=True, key=f"box_{col}")

    st.subheader("📊 Histogramas de Variáveis Quantitativas")
    tabs_hist = st.tabs([f"Hist. {col}" for col in colunas_num])
    for i, col in enumerate(colunas_num):
        with tabs_hist[i]:
            fig = px.histogram(df, x=col, marginal="rug")
            st.plotly_chart(fig, use_container_width=True, key=f"hist_{col}")

    if col_escolaridade and col_escolaridade in df.columns:
        st.subheader("📚 Turnover por Escolaridade")
        esc_counts = df[df[TURNOVER_COL_NAME] == TURNOVER_YES][col_escolaridade].value_counts().reset_index()
        esc_counts.columns = [col_escolaridade, "Desligamentos"]
        fig1 = px.bar(esc_counts, x=col_escolaridade, y="Desligamentos", color=col_escolaridade, text="Desligamentos")
        st.plotly_chart(fig1, use_container_width=True)

    if col_genero and col_genero in df.columns:
        st.subheader("👥 Turnover por Gênero")
        gen_counts = df[df[TURNOVER_COL_NAME] == TURNOVER_YES][col_genero].value_counts().reset_index()
        gen_counts.columns = [col_genero, "Desligamentos"]
        fig2 = px.pie(gen_counts, names=col_genero, values="Desligamentos", hole=0.4)
        st.plotly_chart(fig2, use_container_width=True)


def plot_correlation_heatmap(df):
    st.subheader("🔗 Análise de Correlação (Variáveis Numéricas e Turnover)")
    df_corr = df.copy()

    if df_corr[TURNOVER_COL_NAME].dtype == 'object':
        valid_values = ["Sim", "Não"]
        df_corr = df_corr[df_corr[TURNOVER_COL_NAME].isin(valid_values)]
        df_corr["Turnover_Num"] = df_corr[TURNOVER_COL_NAME].map({"Sim": 1, "Não": 0})
    else:
        df_corr["Turnover_Num"] = df_corr[TURNOVER_COL_NAME]

    colunas_corr = df_corr.select_dtypes(include=np.number).columns.tolist()
    if ID_COL_NAME in colunas_corr:
        colunas_corr.remove(ID_COL_NAME)

    if not colunas_corr:
        st.warning("Não há colunas numéricas suficientes para calcular a correlação.")
        return

    corr = df_corr[colunas_corr].corr()
    fig_corr = px.imshow(corr, text_auto=".2f", aspect="auto", color_continuous_scale='RdBu')
    st.plotly_chart(fig_corr, use_container_width=True)
