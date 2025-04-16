import streamlit as st
import pandas as pd

st.title("📊 SNPIT AMM ダッシュボード - CSV読み込み修正")

try:
    df = pd.read_csv("snpit_amm_log.csv", sep="\t", encoding="utf-8-sig")

    # BOM付きカラム名の修正
    df.rename(columns={df.columns[0]: "date"}, inplace=True)

    # 日付変換
    df["date"] = pd.to_datetime(df["date"], format="%Y/%m/%d", errors="coerce")
    df = df[df["date"].notna()]

    # 数値列を float に変換（安全のため）
    for col in ["balance", "in_total", "in_from_operator", "out_total", "out_to_operator", "number"]:
        df[col] = pd.to_numeric(df[col], errors="coerce")

    st.success("✅ CSV 読み込み成功！")
    st.dataframe(df)

except Exception as e:
    st.error(f"❌ エラー発生: {e}")
