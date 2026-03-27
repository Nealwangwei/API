import streamlit as str
str.title('聊天机器人')
str.divider()
str.chat_message('assistant').write('你好，有什么可以帮助您的吗')
prompt = str.chat_input('请输入您的问题:')
str.chat_message('user').write(prompt)
if prompt:
    str.chat_message('assistant').write('很高兴为你服务')
