# simulator.py
import streamlit as st
import pandas as pd

TURNOVER_COL_NAME = "Turnover"
ID_COL_NAME = "ID"


def run_simulation(model, train_columns, df_model_for_sim):
    if model is None or train_columns is None or df_model_for_sim is None:
        st.info("Modelo não treinado. Simulador indisponível.")
        return

    st.subheader("🧪 Simulador de Perfil de Colaborador")
    st.markdown("Preencha os dados abaixo para prever a probabilidade de saída (Turnover = Sim).")

    input_data = {}
    sim_cols_to_drop = [TURNOVER_COL_NAME, "target"]
    if ID_COL_NAME in df_model_for_sim.columns:
        sim_cols_to_drop.append(ID_COL_NAME)
    sim_cols_to_drop = [col for col in sim_cols_to_drop if col in df_model_for_sim.columns]

    simulation_features = df_model_for_sim.drop(columns=sim_cols_to_drop)
    cols1, cols2 = st.columns(2)

    for i, col in enumerate(simulation_features.columns):
        target_col = cols1 if i % 2 == 0 else cols2
        if simulation_features[col].dtype == 'object':
            unique_vals_raw = simulation_features[col].dropna().unique()
            unique_vals = sorted([str(val) for val in unique_vals_raw])
            try:
                default_val_raw = simulation_features[col].mode()[0]
                default_val_str = str(default_val_raw)
                default_ix = unique_vals.index(default_val_str)
            except Exception:
                default_ix = 0
            input_data[col] = target_col.selectbox(f"{col}", unique_vals, index=default_ix, key=f"sim_{col}")
        elif pd.api.types.is_numeric_dtype(simulation_features[col]):
            default_val = float(simulation_features[col].median())
            min_val = float(simulation_features[col].min())
            max_val = float(simulation_features[col].max())
            input_data[col] = target_col.number_input(f"{col}", value=default_val, min_value=min_val, max_value=max_val, key=f"sim_{col}")

    if st.button("🔍 Prever Turnover", key='predict_button'):
        try:
            input_df = pd.DataFrame([input_data])
            input_encoded = pd.get_dummies(input_df, drop_first=True)
            input_aligned = pd.DataFrame(columns=train_columns)
            input_aligned = pd.concat([input_aligned, input_encoded], axis=0, ignore_index=True)
            input_aligned = input_aligned.fillna(0)
            input_aligned = input_aligned[train_columns]
            input_aligned = input_aligned.iloc[-1:]

            with st.spinner("Calculando previsão..."):
                pred_proba = model.predict_proba(input_aligned)[0][1]

            st.success(f"Probabilidade estimada de saída: {pred_proba * 100:.2f}%")

            if pred_proba > 0.7:
                st.error("ALTA probabilidade de saída.")
            elif pred_proba > 0.4:
                st.warning("MÉDIA probabilidade de saída.")
            else:
                st.info("BAIXA probabilidade de saída.")

        except Exception as e:
            st.error(f"Erro durante a previsão: {e}")
            st.error("Verifique os dados de entrada e se o modelo foi treinado corretamente.")
