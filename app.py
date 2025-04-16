import streamlit as st
import pandas as pd

st.title("📊 SNPIT AMMデータ確認（最小テスト）")

try:
    # タブ区切り + BOM付きCSV想定
    df = pd.read_csv("snpit_amm_log.csv", sep="\t", encoding="utf-8-sig")
    
    # 日付変換
    df["date"] = pd.to_datetime(df["date"], format="%Y/%m/%d", errors="coerce")
    df = df[df["date"].notna()]

    st.write("✅ CSV読み込み成功！")
    st.dataframe(df)

except Exception as e:
    st.error(f"❌ エラー発生: {e}")
