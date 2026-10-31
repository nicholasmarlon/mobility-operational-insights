# -*- coding: utf-8 -*-
import sqlite3
import pandas as pd

def load_trip_data(db_path: str = "data/mobility.db") -> pd.DataFrame:
    """Carrega os dados de corridas do banco SQLite para um DataFrame do Pandas."""
    try:
        conn = sqlite3.connect(db_path)
        query = "SELECT * FROM trips"
        df = pd.read_sql(query, conn)
        conn.close()
        
        if 'timestamp' in df.columns:
            df['timestamp'] = pd.to_datetime(df['timestamp'])
            
        return df
    except Exception as e:
        print(f"⚠️ Erro ao carregar dados do banco: {e}")
        return pd.DataFrame()

def calculate_financial_metrics(df: pd.DataFrame) -> pd.DataFrame:
    """Calcula métricas financeiras, custos de combustível e lucro líquido por corrida (P&L)."""
    if df.empty:
        return df
        
    # Custo de combustível por km (considerando consumo médio de 10 km/L)
    fuel_efficiency_km_per_liter = 10.0
    df['fuel_consumed_liters'] = (df['trip_km'] + df['pickup_km']) / fuel_efficiency_km_per_liter
    df['total_fuel_cost'] = df['fuel_consumed_liters'] * df['fuel_cost_per_liter']
    
    # Lucro Líquido por Corrida ($)
    df['net_fare'] = df['gross_fare'] - df['platform_fee']
    df['net_profit'] = df['net_fare'] - df['total_fuel_cost']
    
    # Rentabilidade por Hora ($/h)
    df['profit_per_hour'] = df.apply(
        lambda row: (row['net_profit'] / (row['duration_minutes'] / 60)) if row['duration_minutes'] > 0 else 0, 
        axis=1
    )
    
    # Rentabilidade por KM ($/km)
    df['profit_per_km'] = df.apply(
        lambda row: (row['net_profit'] / row['trip_km']) if row['trip_km'] > 0 else 0, 
        axis=1
    )
    
    return df

def get_summary_kpis(df: pd.DataFrame) -> dict:
    """Retorna um dicionário com os KPIs consolidados para o dashboard."""
    if df.empty:
        return {
            "total_trips": 0,
            "gross_revenue": 0.0,
            "net_profit": 0.0,
            "avg_profit_per_hour": 0.0,
            "avg_profit_per_km": 0.0
        }
        
    summary = {
        "total_trips": int(len(df)),
        "gross_revenue": float(df['gross_fare'].sum()),
        "net_profit": float(df['net_profit'].sum()),
        "avg_profit_per_hour": float(df['profit_per_hour'].mean()),
        "avg_profit_per_km": float(df['profit_per_km'].mean())
    }
    return summary

if __name__ == "__main__":
    df = load_trip_data()
    if not df.empty:
        df = calculate_financial_metrics(df)
        kpis = get_summary_kpis(df)
        print("📊 KPIs Calculados com Sucesso:")
        for k, v in kpis.items():
            print(f" - {k}: {v}")
    else:
        print("⚠️ Nenhum dado encontrado. Execute o database.py primeiro.")