# db_utils.py

import pandas as pd
from sqlalchemy import create_engine, text
import streamlit as st
import urllib.parse

@st.cache_resource
def get_engine():
    config = st.secrets["mysql"]
    password = urllib.parse.quote_plus(config["password"])

    conn_url = (
        f"mysql+pymysql://{config['user']}:{password}@{config['host']}:{config['port']}/{config['database']}?"
        "connect_timeout=10&read_timeout=30"
    )
    
    return create_engine(
        conn_url,
        pool_pre_ping=True,   # Reconnect automatically if connection is dropped
        pool_recycle=280      # Recycle connection after 280s to avoid timeout
    )

def ensure_table_exists():
    create_table_sql = """
    CREATE TABLE IF NOT EXISTS visitor_feedback (
        id INT AUTO_INCREMENT PRIMARY KEY,
        name VARCHAR(100),
        contact_number VARCHAR(20),
        purpose TEXT,
        mobile_number VARCHAR(20),
        feedback TEXT,
        report_date DATE
    );
    """
    engine = get_engine()
    with engine.begin() as conn:
        conn.execute(text(create_table_sql))

def insert_feedback(data_dict):
    ensure_table_exists()
    df = pd.DataFrame([data_dict])
    df.to_sql("visitor_feedback", con=get_engine(), if_exists="append", index=False, method="multi")

def fetch_all_feedback():
    ensure_table_exists()
    query = "SELECT * FROM visitor_feedback ORDER BY id DESC"
    return pd.read_sql(query, con=get_engine())
