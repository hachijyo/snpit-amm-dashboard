import streamlit as st
import pandas as pd

st.title("CSVフォーマット検証")

try:
    df = pd.read_csv("snpit_amm_log.csv", encoding='utf-8-sig')
    st.write("✅ 読み込み成功")
    st.dataframe(df)
except Exception as e:
    st.error(f"❌ 読み込みエラー: {e}")
