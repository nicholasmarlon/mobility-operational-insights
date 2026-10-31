# -*- coding: utf-8 -*-
import streamlit as st
import pandas as pd
import plotly.express as px
from analytics import load_trip_data, calculate_financial_metrics, get_summary_kpis

st.set_page_config(
    page_title="Mobility Operational Insights",
    page_icon="🚘",
    layout="wide"
)

st.title("🚘 Mobility Operational Insights")
st.markdown("Dashboard executivo para análise de rentabilidade, P&L e inteligência operacional em transporte por aplicativo.")

# Carregar dados
df_raw = load_trip_data()
if df_raw.empty:
    st.warning("⚠️ Nenhum dado encontrado no banco. Execute python src/database.py primeiro.")
else:
    df = calculate_financial_metrics(df_raw)

    # Sidebar Filters
    st.sidebar.header("🔍 Filtros Operacionais")
    selected_platforms = st.sidebar.multiselect(
        "Plataforma",
        options=df['platform'].unique(),
        default=df['platform'].unique()
    )
    
    selected_zones = st.sidebar.multiselect(
        "Zona de Partida",
        options=df['pickup_zone'].unique(),
        default=df['pickup_zone'].unique()
    )

    # Aplicar filtros
    filtered_df = df[
        (df['platform'].isin(selected_platforms)) & 
        (df['pickup_zone'].isin(selected_zones))
    ]

    kpis = get_summary_kpis(filtered_df)

    # Exibir KPIs principais
    st.markdown("### 📊 Indicadores Chave de Desempenho (KPIs)")
    col1, col2, col3, col4, col5 = st.columns(5)
    
    col1.metric("Total de Corridas", f"{kpis['total_trips']}")
    col2.metric("Faturamento Bruto", f"R$ {kpis['gross_revenue']:.2f}")
    col3.metric("Lucro Líquido (P&L)", f"R$ {kpis['net_profit']:.2f}")
    col4.metric("Média / Hora", f"R$ {kpis['avg_profit_per_hour']:.2f}/h")
    col5.metric("Média / KM", f"R$ {kpis['avg_profit_per_km']:.2f}/km")

    st.markdown("---")

    # Gráficos
    col_left, col_right = st.columns(2)

    with col_left:
        st.markdown("### 💰 Lucro Líquido por Zona de Partida")
        if not filtered_df.empty:
            zone_profit = filtered_df.groupby('pickup_zone')['net_profit'].sum().reset_index()
            fig_zone = px.bar(
                zone_profit, 
                x='pickup_zone', 
                y='net_profit', 
                title="Lucro Líquido Total por Zona (R$)",
                labels={'pickup_zone': 'Zona', 'net_profit': 'Lucro Líquido (R$)'},
                color='net_profit',
                color_continuous_scale='Blues'
            )
            st.plotly_chart(fig_zone, use_container_width=True)

    with col_right:
        st.markdown("### 📈 Faturamento por Plataforma")
        if not filtered_df.empty:
            plat_rev = filtered_df.groupby('platform')['gross_fare'].sum().reset_index()
            fig_plat = px.pie(
                plat_rev, 
                names='platform', 
                values='gross_fare', 
                title="Distribuição de Faturamento Bruto por Plataforma",
                hole=0.4
            )
            st.plotly_chart(fig_plat, use_container_width=True)

    st.markdown("---")

    # Calculadora de Viabilidade de Corrida (Simulador)
    st.markdown("### 🧮 Simulador de Viabilidade de Corrida")
    st.markdown("Insira os dados da corrida oferecida para calcular instantaneamente se vale a pena aceitar com base no P&L.")

    sim_col1, sim_col2, sim_col3 = st.columns(3)
    with sim_col1:
        sim_pickup_km = st.number_input("Distância até a Origem (Km)", min_value=0.1, max_value=10.0, value=1.5)
    with sim_col2:
        sim_trip_km = st.number_input("Distância da Corrida (Km)", min_value=1.0, max_value=50.0, value=10.0)
    with sim_col3:
        sim_gross_fare = st.number_input("Valor Ofertado (R$)", min_value=5.0, max_value=200.0, value=25.0)

    fuel_price = 5.89
    fuel_eff = 10.0
    sim_fee_pct = 0.20 # 20% média

    total_km = sim_pickup_km + sim_trip_km
    est_fuel_cost = (total_km / fuel_eff) * fuel_price
    est_fee = sim_gross_fare * sim_fee_pct
    est_net_profit = sim_gross_fare - est_fee - est_fuel_cost
    est_profit_per_km = est_net_profit / sim_trip_km if sim_trip_km > 0 else 0

    sim_res_col1, sim_res_col2, sim_res_col3 = st.columns(3)
    sim_res_col1.metric("Custo Estimado (Combustível)", f"R$ {est_fuel_cost:.2f}")
    sim_res_col2.metric("Lucro Líquido Estimado", f"R$ {est_net_profit:.2f}")
    sim_res_col3.metric("Retorno por KM Rodado", f"R$ {est_profit_per_km:.2f}/km")

    if est_profit_per_km >= 2.50:
        st.success("✅ **Recomendação: EXCELENTE CORRIDA!** Alta margem por quilômetro.")
    elif est_profit_per_km >= 1.50:
        st.info("ℹ️ **Recomendação: CORRIDA VIÁVEL.** Margem dentro da média operacional.")
    else:
        st.error("❌ **Recomendação: RECUSAR.** Baixa rentabilidade líquida para o custo de deslocamento.")