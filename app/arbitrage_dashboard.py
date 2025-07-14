#!/usr/bin/env python3
import os
import asyncio
import pandas as pd
import altair as alt
import streamlit as st
import streamlit.components.v1 as components
from pnl import record_trade, get_pnl

# ────────────────────────────── WALLET CONNECT UI ─────────────────────────────

st.set_page_config(page_title="Arbitrage Dashboard", layout="centered")
st.title("🪙 Crypto Arbitrage Dashboard")
st.write("Track opportunities & profits with wallet status.")

# Visible WalletConnect iframe (replace with your real WC project ID)
WC_PROJECT = st.secrets.get("walletconnect", {}).get("project_id", "")
if WC_PROJECT:
    st.markdown("### 🔌 Connect Wallet via WalletConnect")
    components.html(
        f"""
        <iframe
            src="https://explorer.walletconnect.com/?projectId={WC_PROJECT}&relay-protocol=irn&chain=1"
            width="100%" height="420" frameborder="0"></iframe>
        """,
        height=450,
    )
else:
    st.warning("⚠️ WalletConnect project ID not configured in secrets.")

# Optional: manually enter address
wallet = st.text_input("🧾 Wallet address (optional):", placeholder="0x...")

# ─────────────────────────────── MOCK ARBITRAGE UI ───────────────────────────────

st.markdown("---")
st.subheader("📈 Scan & Log Arbitrage Opportunity")

pair = st.selectbox("Select Pair", ["BTC/USDT", "ETH/USDT", "SOL/USDT"])
buy_px = st.number_input("Buy Price", value=30000.0)
sell_px = st.number_input("Sell Price", value=30500.0)
qty = st.number_input("Trade Size", value=0.1)
spread = round((sell_px - buy_px) / buy_px * 100, 2)

if st.button("🚀 Record Trade"):
    record_trade(pair, buy_px, sell_px, qty, spread)
    st.success(f"Logged trade for {pair} with {spread}% spread")

# ─────────────────────────────── PNL CHART SECTION ───────────────────────────────

st.markdown("---")
st.subheader("📊 Net P&L Chart")

df = get_pnl()
if not df.empty:
    chart = (
        alt.Chart(df)
        .mark_line(point=True)
        .encode(
            x="timestamp:T",
            y="pnl:Q",
            tooltip=["timestamp:T", "pnl:Q"]
        )
        .interactive()
    )
    st.altair_chart(chart, use_container_width=True)
else:
    st.info("No PNL data yet. Record a trade to see chart.")
