import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

# ==== 読み込み＆変換テスト ====
df = pd.read_csv("snpit_amm_log.csv")
df["date"] = pd.to_datetime(df["date"], format="%Y/%m/%d", errors="coerce")
df = df[df["date"].notna()]

# ==== デバッグ表示 ====
st.write("データプレビュー", df.tail())

# ==== 単独グラフのみ表示 ====
st.subheader("SNTP残高の推移")
fig, ax = plt.subplots()
df.plot(x="date", y="balance", ax=ax)
st.pyplot(fig)
