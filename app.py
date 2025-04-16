import streamlit as st
import pandas as pd

st.title("✅ タブ区切りTSV読み込みテスト")

try:
    df = pd.read_csv("snpit_amm_log.csv", sep="\t")  # ← タブ区切り指定！
    df["date"] = pd.to_datetime(df["date"], format="%Y/%m/%d", errors="coerce")
    df = df[df["date"].notna()]
    st.write("📄 読み込み成功！データプレビュー")
    st.dataframe(df)
except Exception as e:
    st.error(f"❌ エラー発生: {e}")
