import streamlit as st
from pydub import AudioSegment
import ffprobe
import os

# ファイルを5分ごとに区切り、"result"フォルダに保存する関数
def split_and_save_audio(input_file, output_folder):
    audio = AudioSegment.from_file(input_file, format='mp3')
    segment_length = 5 * 60 * 1000  # 5分をミリ秒に変換

    # "result"フォルダが存在しない場合は作成
    result_folder = os.path.join(output_folder, "results")
    if not os.path.exists(result_folder):
        os.makedirs(result_folder)

    # 5分ごとに区切り、新しいファイルとして保存
    for i, start_time in enumerate(range(0, len(audio), segment_length)):
        end_time = min(start_time + segment_length, len(audio))
        segment = audio[start_time:end_time]

        # 出力ファイルの名前を生成
        output_file = os.path.join(result_folder, f"segment_{i + 1}.mp3")

        # 新しいファイルとして保存
        segment.export(output_file, format="mp3")

# Streamlitアプリケーションのレイアウト
def main():
    st.title("音声ファイル分割アプリ")

    # ファイルのアップロード
    uploaded_file = st.file_uploader("音声ファイルを選択してください（4分単位で分割します）", type=["mp3"])

    if uploaded_file is not None:
        st.text("ファイルが選択されました.")
        st.text("mp3ファイルを分割中です...")

        # "result"フォルダに保存
        output_folder = os.path.dirname(uploaded_file.name)
        split_and_save_audio(uploaded_file, output_folder)

        st.success(f"分割が完了し、'result'フォルダに保存されました。")

if __name__ == "__main__":
    main()
