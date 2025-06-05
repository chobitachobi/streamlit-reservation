# app.py
import streamlit as st
import pandas as pd
from datetime import date, time, datetime

# データ保存用のCSVファイル
CSV_FILE = "reservations.csv"


# 初期化（ファイルがなければ作る）
def initialize_csv():
    try:
        pd.read_csv(CSV_FILE)
    except FileNotFoundError:
        df = pd.DataFrame(columns=["Name", "Date", "Time"])
        df.to_csv(CSV_FILE, index=False)


# 予約情報を保存
def save_reservation(name, selected_date, selected_time):
    df = pd.read_csv(CSV_FILE)
    new_entry = {
        "Name": name,
        "Date": selected_date.strftime("%Y-%m-%d"),
        "Time": selected_time.strftime("%H:%M"),
    }
    df = pd.concat([df, pd.DataFrame([new_entry])], ignore_index=True)

    df.to_csv(CSV_FILE, index=False)


# 予約の重複をチェック
def is_already_reserved(selected_date, selected_time):
    df = pd.read_csv(CSV_FILE)
    return (
        (df["Date"] == selected_date.strftime("%Y-%m-%d"))
        & (df["Time"] == selected_time.strftime("%H:%M"))
    ).any()


# アプリ本体
def main():
    st.title("📅 簡易予約システム")

    name = st.text_input("お名前を入力してください")
    selected_date = st.date_input("日付を選んでください", min_value=date.today())
    selected_time = st.time_input("時間を選んでください", value=time(10, 0))

    if st.button("予約を確定する"):
        if not name:
            st.warning("お名前を入力してください。")
        elif is_already_reserved(selected_date, selected_time):
            st.error("この時間帯はすでに予約されています。別の時間を選んでください。")
        else:
            save_reservation(name, selected_date, selected_time)
            st.success(
                f"{selected_date} {selected_time.strftime('%H:%M')} に予約を確定しました！"
            )

    # 予約状況の表示（オプション）
    with st.expander("🔍 現在の予約状況を表示"):
        df = pd.read_csv(CSV_FILE)
        st.table(df.sort_values(by=["Date", "Time"]))


if __name__ == "__main__":
    initialize_csv()
    main()
