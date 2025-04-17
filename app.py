import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.ticker as ticker
import matplotlib.dates as mdates
import matplotlib

# ✅ Streamlit Cloud 互換のフォント設定（日本語表示）
matplotlib.rcParams['font.sans-serif'] = ['Noto Sans CJK JP', 'IPAPGothic', 'TakaoGothic', 'VL Gothic', 'DejaVu Sans']
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
    st.subheader("SNPT残高と取引件数の推移")
    fig1, ax1 = plt.subplots(figsize=(10, 5))
    ax1.set_ylabel("取引件数", color='tab:blue')
    ax1.plot(df["date"], df["number"], color='tab:blue')
    ax1.tick_params(axis='y', labelcolor='tab:blue')

    ax2 = ax1.twinx()
    ax2.set_ylabel("SNPT残高（100万単位）", color='tab:orange')
    ax2.plot(df["date"], df["balance_million"], color='tab:orange')
    ax2.yaxis.set_major_formatter(ticker.FuncFormatter(lambda x, _: f'{x:.1f}M'))
    ax2.tick_params(axis='y', labelcolor='tab:orange')

    ax1.xaxis.set_major_locator(mdates.AutoDateLocator())
    ax1.xaxis.set_major_formatter(mdates.DateFormatter('%Y-%m-%d'))
    fig1.autofmt_xdate(rotation=30)
    st.pyplot(fig1)

    # ==== グラフ2 ====
    st.subheader("流入と流出の推移")
    df.rename(columns={"in_total": "流入", "out_total": "流出"}, inplace=True)
    fig2, ax = plt.subplots(figsize=(10, 5))
    ax.plot(df["date"], df["流入"], label="流入", color="tab:orange")
    ax.plot(df["date"], df["流出"], label="流出", color="tab:blue")
    ax.set_ylabel("SNPT")
    ax.legend(title="")
    ax.xaxis.set_major_locator(mdates.AutoDateLocator())
    ax.xaxis.set_major_formatter(mdates.DateFormatter('%Y-%m-%d'))
    fig2.autofmt_xdate(rotation=30)
    st.pyplot(fig2)

    st.success("✅ グラフ表示完了")

except Exception as e:
    st.error(f"❌ エラー発生: {e}")
