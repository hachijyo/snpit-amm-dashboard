import streamlit as st
import os

st.title("📂 ファイル確認テスト")

# カレントディレクトリを表示
cwd = os.getcwd()
st.write("カレントディレクトリ:", cwd)

# ファイル一覧を表示
st.write("ディレクトリ内のファイル一覧:")
st.write(os.listdir(cwd))

# ファイルの存在チェック
csv_path = os.path.join(cwd, "snpit_amm_log.csv")
if os.path.exists(csv_path):
    st.success("✅ snpit_amm_log.csv が見つかりました！")
else:
    st.error("❌ snpit_amm_log.csv が存在しません！")

st.write("👇ファイル一覧がここに見えるはずです。")
