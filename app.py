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
    df["in_other"] = df["in_total"] - df["in_from_operator"]
    df["out_other"] = df["out_total"] - df["out_to_operator"]

    # ==== グラフ1 ====
    fig1, ax1 = plt.subplots(figsize=(6, 4))
    ax1.set_ylabel("torihiki kensu", color='tab:blue')
    ax1.plot(df["date"], df["number"], color='tab:blue', label="torihiki kensu")
    ax1.tick_params(axis='y', labelcolor='tab:blue')

    ax2 = ax1.twinx()
    ax2.set_ylabel("SNPT zandaka", color='tab:orange')
    bar_width = 0.99
    ax2.bar(df["date"], df["balance_million"], width=bar_width, color='tab:orange', alpha=0.6, label="SNPT zandaka")
    ax2.yaxis.set_major_formatter(ticker.FuncFormatter(lambda x, _: f'{x:.1f}M'))
    ax2.tick_params(axis='y', labelcolor='tab:orange')

    ax1.xaxis.set_major_locator(mdates.AutoDateLocator())
    ax1.xaxis.set_major_formatter(mdates.DateFormatter('%Y-%m-%d'))
    for label in ax1.get_xticklabels():
        label.set_rotation(90)

    # ==== グラフ2（積み上げ棒グラフ） ====
    fig2, ax = plt.subplots(figsize=(6, 4))
    # 順番：in_other（上）、in_from_operator（下）、out_other（上）、out_to_operator（下）
    ax.bar(df["date"], df["in_other"] / 1e6, label="in: others", color="#ffd9b3")
    ax.bar(df["date"], df["in_from_operator"] / 1e6, bottom=df["in_other"] / 1e6, label="in: operator", color="orange")
    ax.bar(df["date"], -df["out_other"] / 1e6, label="out: others", color="#b3d1ff")
    ax.bar(df["date"], -df["out_to_operator"] / 1e6, bottom=-df["out_other"] / 1e6, label="out: operator", color="blue")

    ax.axhline(0, color='black', linewidth=0.5)
    ax.set_ylabel("SNPT (Million)")
    ax.yaxis.set_major_formatter(ticker.FuncFormatter(lambda x, _: f'{x:.1f}M'))
    ax.legend(title="")
    ax.xaxis.set_major_locator(mdates.AutoDateLocator())
    ax.xaxis.set_major_formatter(mdates.DateFormatter('%Y-%m-%d'))
    for label in ax.get_xticklabels():
        label.set_rotation(90)

    # ==== 横並びレイアウト ====
    col1, col2 = st.columns(2)

    with col1:
        st.subheader("SNPT残高と取引件数の推移")
        st.pyplot(fig1)

    with col2:
        st.subheader("流入・流出（運営/その他）")
        st.pyplot(fig2)

    st.success("✅ Chart rendering complete")

except Exception as e:
    st.error(f"❌ Error occurred: {e}")