import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

# CSVファイルを読み込む
csv_path = "snpit_amm_log.csv"
df = pd.read_csv(csv_path, parse_dates=["date"])

st.title("SNPIT AMM")

# ==== チャート1: balance と number の推移 ====
st.subheader("SNTP残高とTransfer数の推移")
fig1, ax1 = plt.subplots()
ax1.set_ylabel("Balance (SNTP)", color='tab:blue')
df.plot(x="date", y="balance", ax=ax1, legend=False, color='tab:blue')
ax2 = ax1.twinx()
ax2.set_ylabel("Transfer", color='tab:orange')
df.plot(x="date", y="number", ax=ax2, legend=False, color='tab:orange')
st.pyplot(fig1)

# ==== チャート2: in_total と out_total の推移 ====
st.subheader("流入と流出の推移")
fig2, ax = plt.subplots()
df.plot(x="date", y=["in_total", "out_total"], ax=ax)
ax.set_ylabel("SNTP")
st.pyplot(fig2)

st.caption("データ提供: AMM監視Botより自動収集")
