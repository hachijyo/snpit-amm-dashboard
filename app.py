import streamlit as st
import pandas as pd

st.title("📊 SNPIT AMM CSV読み込みテスト")

try:
    with open("snpit_amm_log.csv", "r", encoding="utf-8-sig") as f:
        lines = f.readlines()

    # タブで分割して DataFrame 化
    data = [line.strip().split("\t") for line in lines if line.strip()]
    headers = data[0]
    rows = data[1:]
    df = pd.DataFrame(rows, columns=headers)

    # 日付を変換
    df["date"] = pd.to_datetime(df["date"], format="%Y/%m/%d", errors="coerce")
    df = df[df["date"].notna()]

    # 数値列を明示的に float に変換（念のため）
    for col in ["balance", "in_total", "in_from_operator", "out_total", "out_to_operator", "number"]:
        df[col] = pd.to_numeric(df[col], errors="coerce")

    st.success("✅ CSV 読み込み成功！")
    st.dataframe(df)

except Exception as e:
    st.error(f"❌ エラー発生: {e}")
