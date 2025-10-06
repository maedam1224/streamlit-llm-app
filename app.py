import os
from dotenv import load_dotenv
import streamlit as st
from langchain.chat_models import ChatOpenAI
from langchain.schema import SystemMessage, HumanMessage

# .envからAPIキーを取得
load_dotenv()
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

# 専門家の種類を定義
EXPERTS = {
    "医療の専門家": "あなたは優秀な医療の専門家です。専門的かつ分かりやすく回答してください。",
    "ITコンサルタント": "あなたは経験豊富なITコンサルタントです。分かりやすく実践的なアドバイスをしてください。"
}

# LLM呼び出し関数
def ask_llm(input_text: str, expert_type: str) -> str:
    system_message = SystemMessage(content=EXPERTS[expert_type])
    human_message = HumanMessage(content=input_text)
    llm = ChatOpenAI(openai_api_key=OPENAI_API_KEY)
    response = llm([system_message, human_message])
    return response.content

# Streamlitアプリ
st.title("専門家AIチャットアプリ")
st.markdown("""
このアプリは、入力した質問や相談内容に対して、選択した分野の専門家としてAIが回答します。（医療の専門家またはITコンサルタント）

【使い方】
1. 下のラジオボタンで相談したい専門家の分野を選択してください。
2. テキスト入力欄に質問や相談内容を入力し、「送信」ボタンを押してください。
3. AIによる専門的な回答が画面下部に表示されます。
""")

# 専門家選択
expert_type = st.radio("専門家を選択してください", list(EXPERTS.keys()))

# 入力フォーム
input_text = st.text_area("質問・相談内容を入力してください")

if st.button("送信"):
    if not input_text.strip():
        st.warning("質問内容を入力してください。")
    else:
        with st.spinner("AIが回答中..."):
            answer = ask_llm(input_text, expert_type)
        st.success("AIの回答:")
        st.write(answer)

