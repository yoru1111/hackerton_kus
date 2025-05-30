import streamlit as st
import google.generativeai as genai
from pathlib import Path

# 페이지 설정
st.set_page_config(
    page_title="Gemini AI Chat",
    page_icon="🤖",
    layout="centered"
)

# API 키 불러오기
api_key = None

# Streamlit Cloud 환경
if 'GEMINI_API_KEY' in st.secrets:
    api_key = st.secrets['GEMINI_API_KEY']
# 로컬 환경
else:
    secrets_path = Path(".streamlit/secrets.toml")
    if secrets_path.exists():
        try:
            with open(secrets_path, "r") as f:
                for line in f:
                    if line.startswith("GEMINI_API_KEY"):
                        api_key = line.split("=")[1].strip().strip('"').strip("'")
                        break
        except Exception as e:
            st.error(f"secrets.toml 파일을 읽는 중 오류가 발생했습니다: {str(e)}")
            st.stop()

if not api_key:
    st.error("API 키가 설정되지 않았습니다. Streamlit Cloud의 Secrets에서 GEMINI_API_KEY를 설정하거나, 로컬의 .streamlit/secrets.toml 파일을 확인해주세요.")
    st.stop()

# Gemini 설정
genai.configure(api_key=api_key)
model = genai.GenerativeModel('models/gemini-1.5-flash')

# 채팅 세션 초기화
if "chat" not in st.session_state:
    st.session_state.chat = model.start_chat(history=[])

# 메시지 저장 세션 초기화
if "messages" not in st.session_state:
    st.session_state.messages = []

# 타이틀 및 안내
st.title("🤖 Gemini AI Chat")
st.markdown("Powered by Google's Gemini 1.5 Flash. 시작하려면 아래에 메시지를 입력해보세요.")

# 이전 메시지 보여주기
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# 사용자 입력 받기
if prompt := st.chat_input("메시지를 입력하세요..."):
    # 사용자 메시지 표시
    with st.chat_message("user"):
        st.markdown(prompt)
    st.session_state.messages.append({"role": "user", "content": prompt})

    try:
        # Gemini 응답 생성
        response = st.session_state.chat.send_message(prompt)

        # Gemini 응답 표시
        with st.chat_message("assistant"):
            st.markdown(response.text)
        st.session_state.messages.append({"role": "assistant", "content": response.text})

    except Exception as e:
        error_text = f"❌ 오류 발생: {str(e)}"
        st.error(error_text)
        st.session_state.messages.append({"role": "assistant", "content": error_text})
