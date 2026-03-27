import streamlit as st
import ollama

# 页面配置
st.set_page_config(
    page_title="DeepSeek AI Chat",
    page_icon="🤖",
)

st.title("🤖 웨이가 만든 AI 쳇봇")

# 初始化聊天记录
if "messages" not in st.session_state:
    st.session_state.messages = []

# 显示历史消息
for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])

# 用户输入框
prompt = st.chat_input("여기 질문하세요...")

if prompt:
    # 显示用户消息
    st.chat_message("user").markdown(prompt)

    # 保存用户消息
    st.session_state.messages.append(
        {"role": "user", "content": prompt}
    )

    # AI 回复区域
    with st.chat_message("assistant"):
        message_placeholder = st.empty()
        full_response = ""

        # ⭐ 调用 deepseek（流式输出）
        stream = ollama.chat(
            model="qwen3.5:0.8b",
            messages=st.session_state.messages,
            stream=True,
        )

        for chunk in stream:
            full_response += chunk["message"]["content"]
            message_placeholder.markdown(full_response + "▌")

        message_placeholder.markdown(full_response)

    # 保存AI回复
    st.session_state.messages.append(
        {"role": "assistant", "content": full_response}
    )
