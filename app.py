import streamlit as st
import google.generativeai as genai
import os
from pathlib import Path
import toml

# 페이지 설정
st.set_page_config(
    page_title="Gemini AI Chat",
    page_icon="🤖",
    layout="centered"
)

# API 키 설정
try:
    api_key = st.secrets["GEMINI_API_KEY"]
except Exception as e:
    st.error("API 키가 설정되지 않았습니다. Streamlit Cloud의 Secrets에서 GEMINI_API_KEY를 설정하거나, 로컬의 .streamlit/secrets.toml 파일을 확인해주세요.")
    st.stop()

# Gemini AI 설정
genai.configure(api_key=api_key)

# 채팅 모델 설정 (gemini-1.5-flash로 수정됨)
model = genai.GenerativeModel('gemini-1.5-flash')

# 채팅 기록 초기화
if "chat" not in st.session_state:
    st.session_state.chat = model.start_chat(history=[])

# 페이지 타이틀 및 소개
st.title("🤖 Gemini AI Chat")
st.markdown("""
Welcome to Gemini AI Chat! This is a simple chatbot interface powered by Google's Gemini AI (1.5 Flash).
Feel free to start a conversation below.
""")

# 세션 상태 초기화 (메시지 기록 저장용)
if "messages" not in st.session_state:
    st.session_state.messages = []

# 이전 메시지 표시
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# 사용자 입력 처리
if prompt := st.chat_input("메시지를 입력하세요..."):
    # 사용자 메시지 표시
    with st.chat_message("user"):
        st.markdown(prompt)
    
    # 메시지 기록 저장
    st.session_state.messages.append({"role": "user", "content": prompt})
    
    try:
        # Gemini AI로 응답 생성
        with st.chat_message("assistant"):
            response = st.session_state.chat.send_message(prompt)
            st.markdown(response.text)
        
        # 응답 저장
        st.session_state.messages.append({"role": "assistant", "content": response.text})
    
    except Exception as e:
        error_message = f"❌ 오류 발생: {str(e)}"
        st.error(error_message)
        st.session_state.messages.append({"role": "assistant", "content": error_message})
