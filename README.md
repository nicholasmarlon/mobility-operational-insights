# 🚘 Mobility Operational Insights

> **Pipeline de Engenharia de Dados, Análise Financeira (P&L) e Dashboard Interativo para Otimização Operacional em Transporte por Aplicativo.**

---

## 📌 Visão Geral do Projeto

O **Mobility Operational Insights** é uma solução completa de inteligência de negócios (*Business Intelligence*) e engenharia de dados desenvolvida para transformar dados operacionais brutos de transporte por aplicativo em insights estratégicos de rentabilidade.

A aplicação simula e analisa a mecânica algorítmica por trás da precificação dinâmica, eficiência de rotas, taxa de ocupação e impacto do combustível/manutenção por quilômetro rodado. O sistema centraliza os registros em um banco de dados relacional **SQLite**, processa as métricas via **Python (Pandas)** e entrega um dashboard interativo executivo em **Streamlit**.

---

## 🏗️ Arquitetura da Solução

```text
[ Dados Brutos / Simulação ] 
              │
              ▼
    [ Python ETL / Pandas ] ────► [ Banco Relacional SQLite (mobility.db) ]
                                                │
                                                ▼
                                    [ Motor Analítico (analytics.py) ]
                                                │
                                                ▼
                                    [ Interface Streamlit Web App (app.py) ]
```

---

## 📂 Estrutura Completa do Repositório

```text
mobility-operational-insights/
├── data/
│   └── mobility.db               # Banco de dados SQLite relacional (armazena viagens e custos)
├── src/
│   ├── database.py               # Script de ETL: cria o banco relacional e popula dados operacionais
│   ├── analytics.py              # Motor de cálculos analíticos: DRE, P&L, margens por KM e por Hora
│   └── app.py                    # Aplicação Web Interativa em Streamlit (Dashboard Executivo)
├── requirements.txt              # Dependências e bibliotecas do projeto Python
└── README.md                     # Documentação oficial do projeto
```

---

## ⚙️ Detalhamento dos Módulos

### 1. `src/database.py` (Engenharia de Dados & ETL)
* Responsável pela criação da estrutura relacional no SQLite.
* Injeta e estrutura dados simulados de corridas, considerando variáveis reais como horários de pico, quilometragem percorrida, tarifas dinâmicas (*surge pricing*) e custos operacionais de combustível e manutenção.

### 2. `src/analytics.py` (Motor Analítico & P&L)
* Processa o DataFrame consolidado utilizando **Pandas**.
* Calcula métricas financeiras essenciais:
  * **Faturamento Líquido:** Desconto das taxas da plataforma sobre o valor bruto.
  * **Custo Operacional Total (TCO):** Impacto proporcional do combustível e desgaste mecânico por quilômetro rodado.
  * **Lucro Líquido por Corrida:** Faturamento líquido menos custos operacionais.
  * **Eficiência Temporal e Espacial:** Retorno financeiro por hora trabalhada ($/h) e por quilômetro rodado ($/km).

### 3. `src/app.py` (Dashboard Executivo Interativo)
* Interface construída em **Streamlit**.
* Apresenta gráficos dinâmicos e cartões de KPIs consolidados para apoiar decisões logísticas e financeiras em tempo real.

---

## 📊 Principais KPIs Acompanhados

* **Faturamento Bruto vs. Líquido:** Visão clara da retenção real após taxas de aplicativo.
* **Margem por Hora ($/h) e por KM ($/km):** Identificação de janelas horárias e rotas mais lucrativas.
* **Análise de Tempo Morto:** Rastreamento do custo de deslocamento sem passageiro.
* **Calculadora de Viabilidade:** Ferramenta interativa de suporte à aceitação de chamadas.

---

## 🛠️ Stack Tecnológica

* **Linguagem:** Python 3.10+
* **Manipulação & Análise de Dados:** Pandas, NumPy
* **Armazenamento:** SQLite 3
* **Interface & Visualização:** Streamlit, Plotly Express
* **Controle de Versão:** Git, GitHub, Markdown

---

## 🚀 Como Executar o Projeto Localmente

1. **Clonar o repositório:**
   ```bash
   git clone [https://github.com/nicholasmarlon/mobility-operational-insights.git](https://github.com/nicholasmarlon/mobility-operational-insights.git)
   cd mobility-operational-insights
   ```

2. **Instalar as dependências:**
   ```bash
   py -m pip install -r requirements.txt
   ```

3. **Inicializar o Banco de Dados (ETL):**
   ```bash
   py src/database.py
   ```

4. **Executar o Dashboard no Streamlit:**
   ```bash
   py -m streamlit run src/app.py
   ```

---

## 👨‍💻 Autor

**Nicholas Marlon Barbosa de Souza**  
Graduado em Ciência de Dados e Gestão de TI  
* [LinkedIn](https://www.linkedin.com/in/nicholas-marlon-barbosa-de-souza-169b598b)  
* [GitHub](https://github.com/nicholasmarlon)