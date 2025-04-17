import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.ticker as ticker
import matplotlib

# ✅ 日本語フォント指定（Streamlit Cloud対応）
matplotlib.rcParams['font.family'] = 'Noto Sans CJK JP'

st.title("📊 SNPIT AMM")

try:
    # CSV読み込み
    df = pd.read_csv("snpit_amm_log.csv", sep=",", encoding="utf-8-sig")
    df["date"] = pd.to_datetime(df["date"], errors="coerce")
    df = df[df["date"].notna()]

    # 数値変換
    for col in ["balance", "in_total", "in_from_operator", "out_total", "out_to_operator", "number"]:
        df[col] = pd.to_numeric(df[col], errors="coerce")

    # SNPT残高を100万単位に変換
    df["balance_million"] = df["balance"] / 1e6

    # ==== グラフ1: 取引件数とSNPT残高 ====
    st.subheader("SNPT残高と取引件数の推移")
    fig1, ax1 = plt.subplots()
    ax1.set_ylabel("取引件数", color='tab:blue')
    df.plot(x="date", y="number", ax=ax1, legend=False, color='tab:blue')
    ax1.tick_params(axis='y', labelcolor='tab:blue')

    ax2 = ax1.twinx()
    ax2.set_ylabel("SNPT残高（100万単位）", color='tab:orange')
    df.plot(x="date", y="balance_million", ax=ax2, legend=False, color='tab:orange')
    ax2.yaxis.set_major_formatter(ticker.FuncFormatter(lambda x, _: f'{x:.1f}M'))
    ax2.tick_params(axis='y', labelcolor='tab:orange')
    ax1.get_legend().remove() if ax1.get_legend() else None
    ax2.get_legend().remove() if ax2.get_legend() else None
    st.pyplot(fig1)

    # ==== グラフ2: 流入と流出 ====
    st.subheader("流入と流出の推移")
    fig2, ax = plt.subplots()
    df.rename(columns={"in_total": "流入", "out_total": "流出"}, inplace=True)
    df.plot(x="date", y=["流入", "流出"], ax=ax, color=["tab:orange", "tab:blue"])
    ax.set_ylabel("SNPT")
    if ax.get_legend():
        ax.get_legend().set_title("")
    st.pyplot(fig2)

    st.success("✅ グラフ表示完了！")

except Exception as e:
    st.error(f"❌ エラー発生: {e}")
