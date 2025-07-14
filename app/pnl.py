from datetime import datetime
import os, sqlalchemy as sa, pandas as pd

DB_URL = os.getenv("DATABASE_URL", "sqlite:///pnl.db")
engine = sa.create_engine(DB_URL, future=True)

def _ensure_table():
    with engine.begin() as conn:
        conn.exec_text(
            """CREATE TABLE IF NOT EXISTS pnl (
                   id INTEGER PRIMARY KEY AUTOINCREMENT,
                   ts TIMESTAMP,
                   pair TEXT,
                   gross REAL,
                   fees REAL,
                   net REAL
               )"""
        )
_ensure_table()

def record_trade(pair, buy_px, sell_px, qty, spread):
    gross = (sell_px - buy_px) * qty
    fees = 0.0005 * qty * (buy_px + sell_px)
    net = gross - fees
    with engine.begin() as conn:
        conn.exec_text(
            "INSERT INTO pnl (ts, pair, gross, fees, net) VALUES (:ts,:pair,:g,:f,:n)",
            {"ts": datetime.utcnow(), "pair": pair, "g": gross, "f": fees, "n": net},
        )

def get_pnl():
    with engine.connect() as conn:
        df = pd.read_sql("SELECT ts as timestamp, net as pnl FROM pnl ORDER BY ts", conn)
    return df
