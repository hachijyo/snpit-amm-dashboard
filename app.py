import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.ticker as ticker
import matplotlib.dates as mdates
import matplotlib

matplotlib.rcParams['axes.unicode_minus'] = False

st.set_page_config(page_title="SNPIT AMM", layout="wide")
st.title("📊 SNPIT AMM")

try:
    df = pd.read_csv("snpit_amm_log.csv", encoding="utf-8-sig")
    df["date"] = pd.to_datetime(df["date"], errors="coerce")
    df = df[df["date"].notna()]

    for col in ["balance", "in_total", "in_from_operator", "out_total", "out_to_operator", "number"]:
        df[col] = pd.to_numeric(df[col], errors="coerce")

    df = df.sort_values("date")

    df["balance_million"] = df["balance"] / 1e6
    df["in_user"] = df["in_total"] - df["in_from_operator"]
    df["out_user"] = df["out_total"] - df["out_to_operator"]

    # ==== 表を表示 ====
    display_df = df[[
    "date",               # 日付
    "snpt",               # トークン価格
    "rate",               # 任意のレート評価
    "balance",            # SNPT残高
    "number",             # 取引件数
    "event",              # イベント記録
    "memo",               # 備考
    "in_total",           # 総流入
    "in_from_operator",   # 運営からの流入
    "out_total",          # 総流出
    "out_to_operator"     # 運営への流出
    ]].copy()


    display_df = display_df.sort_values("date", ascending=False)
    display_df["date"] = display_df["date"].dt.date
    display_df[["balance", "in_total", "in_from_operator", "out_total", "out_to_operator", "number"]] = \
        display_df[["balance", "in_total", "in_from_operator", "out_total", "out_to_operator", "number"]].round(0).astype("Int64")

    # 上書き処理は削除済み（以下は削除）
    # display_df["rate"] = ""
    # display_df["event"] = ""
    # display_df["memo"] = ""

    st.dataframe(display_df, use_container_width=True, height=400)


    # ==== グラフ1 ====
    fig1, ax1 = plt.subplots(figsize=(6, 4))
    ax1.set_ylabel("torihiki kensu", color='tab:blue')
    ax1.plot(df["date"], df["number"], color='tab:blue', label="torihiki kensu")
    ax1.tick_params(axis='y', labelcolor='tab:blue')

    ax2 = ax1.twinx()
    ax2.set_ylabel("SNPT zandaka", color='tab:orange')
    bar_width = 0.99
    ax2.bar(df["date"], df["balance_million"], width=bar_width, color='tab:orange', alpha=0.6, label="SNPT zandaka")
    ax2.yaxis.set_major_formatter(ticker.FuncFormatter(lambda x, _: f'{x:.0f}M'))
    ax2.tick_params(axis='y', labelcolor='tab:orange')

    ax1.xaxis.set_major_locator(mdates.AutoDateLocator())
    ax1.xaxis.set_major_formatter(mdates.DateFormatter('%Y-%m-%d'))
    for label in ax1.get_xticklabels():
        label.set_rotation(90)

    # ==== グラフ2（積み上げ棒グラフ）====
    fig2, ax = plt.subplots(figsize=(6, 4))
    ax.bar(df["date"], df["in_from_operator"] / 1e6, label="in: operator", color="orange")
    ax.bar(df["date"], df["in_user"] / 1e6, bottom=df["in_from_operator"] / 1e6, label="in: user", color="#ffd9b3")
    ax.bar(df["date"], -df["out_to_operator"] / 1e6, label="out: operator", color="blue")
    ax.bar(df["date"], -df["out_user"] / 1e6, bottom=-df["out_to_operator"] / 1e6, label="out: user", color="#b3d1ff")

    ax.axhline(0, color='black', linewidth=0.5)
    ax.set_ylabel("SNPT")
    ax.yaxis.set_major_formatter(ticker.FuncFormatter(lambda x, _: f'{x:.0f}M'))

    handles, labels = ax.get_legend_handles_labels()
    order = ['in: user', 'in: operator', 'out: operator', 'out: user']
    sorted_handles = [h for l in order for h, label in zip(handles, labels) if label == l]
    sorted_labels = order
    ax.legend(sorted_handles, sorted_labels, title="")

    ax.xaxis.set_major_locator(mdates.AutoDateLocator())
    ax.xaxis.set_major_formatter(mdates.DateFormatter('%Y-%m-%d'))
    for label in ax.get_xticklabels():
        label.set_rotation(90)


    # ==== グラフ3（トークン価格と比率）====
    fig3, ax1 = plt.subplots(figsize=(6, 4))

    # SNPT価格（左軸）
    ax1.plot(df["date"], df["snpt"], color="blue", label="SNPT")
    ax1.set_ylabel("SNPT", color="blue")
    ax1.tick_params(axis="y", labelcolor="blue")

    # 比率（右軸）
    ax2 = ax1.twinx()
    ax2.plot(df["date"], df["rate"], color="orange", label="Rate")
    ax2.set_ylabel("Rate", color="orange")
    ax2.tick_params(axis="y", labelcolor="orange")

    # X軸設定
    ax1.xaxis.set_major_locator(mdates.AutoDateLocator())
    ax1.xaxis.set_major_formatter(mdates.DateFormatter('%Y-%m-%d'))
    for label in ax1.get_xticklabels():
        label.set_rotation(90)

    # ==== 2行目（横2列：左にグラフ3）====
    row2_col1, row2_col2 = st.columns(2)

    with row2_col1:
        st.subheader("SNPT価格と交換レートの推移")
        st.pyplot(fig3)



    # ==== 横並びレイアウト ====
    row3_col1, row3_col2 = st.columns(2)

    with row3_col1:
        st.subheader("SNPT残高と取引件数の推移")
        st.pyplot(fig1)

    with row3_col2:
        st.subheader("SNPT流入・流出（うち運営※operator）")
        st.pyplot(fig2)

    st.success("✅ Chart rendering complete")

except Exception as e:
    st.error(f"❌ Error occurred: {e}")
