import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

st.title("📊 SNPIT AMM ダッシュボード")

try:
    # タブ区切り + BOM対策
    df = pd.read_csv("snpit_amm_log.csv", sep="\t", encoding="utf-8-sig")
    df.rename(columns={df.columns[0]: "date"}, inplace=True)  # BOM除去

    # 日付変換
    df["date"] = pd.to_datetime(df["date"], format="%Y/%m/%d", errors="coerce")
    df = df[df["date"].notna()]

    # 数値カラムをfloatに変換
    for col in ["balance", "in_total", "in_from_operator", "out_total", "out_to_operator", "number"]:
        df[col] = pd.to_numeric(df[col], errors="coerce")

    # ==== グラフ1: SNTP残高とTransfer数 ====
    st.subheader("SNTP残高とTransfer数の推移")
    fig1, ax1 = plt.subplots()
    ax1.set_ylabel("Balance", color='tab:blue')
    df.plot(x="date", y="balance", ax=ax1, legend=False, color='tab:blue')
    ax2 = ax1.twinx()
    ax2.set_ylabel("Transfer", color='tab:orange')
    df.plot(x="date", y="number", ax=ax2, legend=False, color='tab:orange')
    st.pyplot(fig1)

    # ==== グラフ2: in_total と out_total ====
    st.subheader("流入と流出の推移")
    fig2, ax = plt.subplots()
    df.plot(x="date", y=["in_total", "out_total"], ax=ax)
    ax.set_ylabel("SNTP")
    st.pyplot(fig2)

    st.success("✅ 表示完了！")

except Exception as e:
    st.error(f"❌ エラー発生: {e}")
