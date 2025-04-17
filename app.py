import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.ticker as ticker
import matplotlib.dates as mdates
import matplotlib

matplotlib.rcParams['axes.unicode_minus'] = False

st.set_page_config(page_title="SNPIT AMM", layout="wide")
st.title("📊 SNPIT AMM")

try:
    df = pd.read_csv("snpit_amm_log.csv", encoding="utf-8-sig")
    df["date"] = pd.to_datetime(df["date"], errors="coerce")
    df = df[df["date"].notna()]

    for col in ["balance", "in_total", "in_from_operator", "out_total", "out_to_operator", "number"]:
        df[col] = pd.to_numeric(df[col], errors="coerce")

    df["balance_million"] = df["balance"] / 1e6

    # ==== グラフ1 ====
    st.subheader("SNPT zandaka to torihiki kensu no suii")
    fig1, ax1 = plt.subplots(figsize=(10, 5))
    ax1.set_ylabel("torihiki kensu", color='tab:blue')
    ax1.plot(df["date"], df["number"], color='tab:blue')
    ax1.tick_params(axis='y', labelcolor='tab:blue')

    ax2 = ax1.twinx()
    ax2.set_ylabel("SNPT zandaka", color='tab:orange')
    ax2.plot(df["date"], df["balance_million"], color='tab:orange')
    ax2.yaxis.set_major_formatter(ticker.FuncFormatter(lambda x, _: f'{x:.1f}M'))
    ax2.tick_params(axis='y', labelcolor='tab:orange')

    ax1.xaxis.set_major_locator(mdates.AutoDateLocator())
    ax1.xaxis.set_major_formatter(mdates.DateFormatter('%Y-%m-%d'))
    for label in ax1.get_xticklabels():
        label.set_rotation(90)
    st.pyplot(fig1)

    # ==== グラフ2 ====
    st.subheader("SNPT IN / OUT")
    df.rename(columns={"in_total": "SNPT IN", "out_total": "SNPT OUT"}, inplace=True)
    fig2, ax = plt.subplots(figsize=(10, 5))
    ax.plot(df["date"], df["SNPT IN"], label="SNPT IN", color="tab:orange")
    ax.plot(df["date"], df["SNPT OUT"], label="SNPT OUT", color="tab:blue")
    ax.set_ylabel("SNPT")
    ax.legend(title="")
    ax.xaxis.set_major_locator(mdates.AutoDateLocator())
    ax.xaxis.set_major_formatter(mdates.DateFormatter('%Y-%m-%d'))
    for label in ax.get_xticklabels():
        label.set_rotation(90)
    st.pyplot(fig2)

    st.success("✅ Chart rendering complete")

except Exception as e:
    st.error(f"❌ Error occurred: {e}")