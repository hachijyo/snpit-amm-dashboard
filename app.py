import streamlit as st
import pandas as pd
import os

st.title("SNPIT AMM CSV読み込みテスト")

if not os.path.exists("snpit_amm_log.csv"):
    st.error("❌ エラー: snpit_amm_log.csv が見つかりません。リポジトリにアップロードされていますか？")
else:
    df = pd.read_csv("snpit_amm_log.csv", sep="\t", encoding="utf-8-sig")
    df["date"] = pd.to_datetime(df["date"], format="%Y/%m/%d", errors="coerce")
    df = df[df["date"].notna()]
    st.success("✅ 読み込み成功")
    st.dataframe(df)
