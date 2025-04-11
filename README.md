# 📊 Painel de Turnover (Streamlit + Machine Learning)

Este projeto é um dashboard interativo e preditivo desenvolvido em Python com Streamlit, ideal para análise de turnover em times de RH.

---

## 🚀 Funcionalidades

- Upload da base de dados em Excel
- Filtros interativos por variáveis categóricas
- KPIs dinâmicos
- Gráficos exploratórios e análises estatísticas
- Mapa de correlação
- Modelo preditivo com RandomForest
- Simulador de perfil para previsão de saída

---

## 🧱 Estrutura Modular

```
turnover_dashboard/
├── app.py                 # Arquivo principal do Streamlit
├── data_loader.py         # Carregamento e renomeação de colunas
├── filters.py             # Aplicação de filtros
├── kpis.py                # Exibição de KPIs
├── visualizations.py      # Gráficos e correlação
├── model.py               # Treinamento e avaliação do modelo
├── simulator.py           # Simulador de perfil
├── requirements.txt       # Bibliotecas necessárias
```

---

## ▶️ Como executar

1. Clone o repositório:
```bash
git clone https://github.com/seu-usuario/seu-repositorio.git
cd turnover_dashboard
```

2. Crie seu ambiente virtual e ative (opcional):
```bash
python -m venv .venv
source .venv/bin/activate  # ou .venv\Scripts\activate no Windows
```

3. Instale as dependências:
```bash
pip install -r requirements.txt
```

4. Rode o app:
```bash
streamlit run app.py
```

---

## ✍️ Autor

Rafael E. Oliveira — Engenheiro Civil e Cientista de Dados  
[https://github.com/rafaeeo](https://github.com/rafaeeo)