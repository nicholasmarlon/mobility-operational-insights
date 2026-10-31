\# 🚘 Mobility Operational Insights



> \*\*Pipeline de Engenharia de Dados, Análise Financeira (P\&L) e Dashboard Interativo para Otimização Operacional em Transporte por Aplicativo.\*\*



\---



\## 📌 Visão Geral do Projeto



O \*\*Mobility Operational Insights\*\* é uma solução completa de inteligência de negócios (\*Business Intelligence\*) e engenharia de dados desenvolvida para transformar dados operacionais brutos de transporte por aplicativo em insights estratégicos de rentabilidade.



A aplicação simula e analisa a mecânica algorítmica por trás da precificação dinâmica, eficiência de rotas, taxa de ocupação e impacto do combustível/manutenção por quilômetro rodado. O sistema centraliza os registros em um banco de dados relacional \*\*SQLite\*\*, processa as métricas via \*\*Python (Pandas)\*\* e entrega um dashboard interativo executivo em \*\*Streamlit\*\*.



\---



\## 🏗️ Arquitetura da Solução



```text

\[ Dados Brutos (CSV/Events) ] 

&#x20;             │

&#x20;             ▼

&#x20;   \[ Python ETL / Pandas ] ────► \[ Banco Relacional SQLite ]

&#x20;                                               │

&#x20;                                               ▼

&#x20;                                   \[ Motor Analítico (Analytics) ]

&#x20;                                               │

&#x20;                                               ▼

&#x20;                                   \[ Interface Streamlit Web App ]

