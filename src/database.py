# -*- coding: utf-8 -*-
import sqlite3
import os
import random
from datetime import datetime, timedelta
import pandas as pd

def create_database(db_path: str = "data/mobility.db"):
    """Cria o banco de dados SQLite e a estrutura da tabela de corridas."""
    os.makedirs(os.path.dirname(db_path), exist_ok=True)
    
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS trips (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            timestamp DATETIME NOT NULL,
            platform TEXT NOT NULL,
            pickup_zone TEXT NOT NULL,
            dropoff_zone TEXT NOT NULL,
            pickup_km REAL NOT NULL,
            trip_km REAL NOT NULL,
            duration_minutes INTEGER NOT NULL,
            gross_fare REAL NOT NULL,
            platform_fee REAL NOT NULL,
            fuel_cost_per_liter REAL NOT NULL,
            is_surge INTEGER NOT NULL
        )
    ''')
    
    conn.commit()
    conn.close()
    print(f"✅ Banco de dados e tabela criados com sucesso em: {db_path}")

def populate_sample_data(db_path: str = "data/mobility.db", num_records: int = 100):
    """Gera dados simulados de corridas realistas e insere no banco SQLite."""
    platforms = ['Uber', '99Pop', 'Privado Executivo']
    zones = ['Centro', 'Praia do Morro', 'Enseada Azul', 'Muquiçaba', 'Aeroporto / Vitória']
    
    base_date = datetime.now() - timedelta(days=30)
    data = []
    
    random.seed(42)
    
    for i in range(num_records):
        trip_date = base_date + timedelta(
            days=random.randint(0, 30),
            hours=random.randint(6, 23),
            minutes=random.randint(0, 59)
        )
        
        platform = random.choice(platforms)
        pickup_zone = random.choice(zones)
        dropoff_zone = random.choice([z for z in zones if z != pickup_zone])
        
        pickup_km = round(random.uniform(0.5, 4.0), 2)
        trip_km = round(random.uniform(3.0, 25.0), 2)
        duration_minutes = int(trip_km * random.uniform(1.8, 3.0))
        
        is_surge = 1 if trip_date.hour in [7, 8, 17, 18, 22] else 0
        surge_multiplier = random.uniform(1.2, 1.8) if is_surge else 1.0
        
        rate_per_km = 2.20 * surge_multiplier
        gross_fare = round((trip_km * rate_per_km) + random.uniform(2.5, 5.0), 2)
        
        fee_pct = 0.0 if platform == 'Privado Executivo' else random.uniform(0.18, 0.28)
        platform_fee = round(gross_fare * fee_pct, 2)
        
        fuel_cost_per_liter = 5.89
        
        data.append((
            trip_date.strftime('%Y-%m-%d %H:%M:%S'),
            platform,
            pickup_zone,
            dropoff_zone,
            pickup_km,
            trip_km,
            duration_minutes,
            gross_fare,
            platform_fee,
            fuel_cost_per_liter,
            is_surge
        ))
        
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    cursor.execute("DELETE FROM trips")
    
    cursor.executemany('''
        INSERT INTO trips (
            timestamp, platform, pickup_zone, dropoff_zone,
            pickup_km, trip_km, duration_minutes, gross_fare,
            platform_fee, fuel_cost_per_liter, is_surge
        ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
    ''', data)
    
    conn.commit()
    conn.close()
    print(f"🚀 {num_records} registros de corridas inseridos no SQLite!")

if __name__ == "__main__":
    create_database()
    populate_sample_data()