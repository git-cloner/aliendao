from openai import OpenAI
import streamlit as st
import streamlit.components.v1 as components
import random

client = OpenAI(
    base_url="https://gitclone.com/aiit/ollama/v1",
    api_key="EMPTY")


def clear_chat_history():
    st.session_state.messages = [
        {"role": "assistant", "content": ""}
    ]
    setInputFocus()


def init_page():
    st.set_page_config(
        page_title="AI Chatbot",
        page_icon=" ",
        layout="wide",
    )


def init_sidebar():
    st.sidebar.title('AI Chatbot')
    st.markdown(
        """  
        <style>  
        .st-emotion-cache-1huvf7z {display: none;}  
        .st-emotion-cache-w3nhqi {display: none;}  
        </style>  
        """,
        unsafe_allow_html=True
    )
    # 选择模型
    model_options = ('glm4', 'llama3.2', 'gemma2',
                     'qwen2.5', 'phi3.5', 'mistral-small',
                     'deepseek-coder-v2')
    selected_model = st.sidebar.radio(
        label='选择模型',
        options=model_options,
        index=0,
        format_func=str,
        help='',
        key='selected_model', on_change=model_changed)
    # 温度
    temperature = st.sidebar.slider(
        '温度', min_value=0.01, max_value=1.0, value=0.9, step=0.1, key='temperature')
    # top_p
    top_p = st.sidebar.slider('累计概率采样', min_value=0.01,
                              max_value=1.0, value=0.9, step=0.1, key='top_p')
    # 最大长度
    max_length = st.sidebar.slider(
        '最大长度', min_value=64, max_value=4096, value=512, step=8, key='max_length')
    # 清除聊天历史
    st.sidebar.button('清除会话记录', on_click=clear_chat_history)
    st.sidebar.markdown(f'''
        <a href={'https://gitclone.com/aiit/chat/'}>旧版</a>
        ''',
        unsafe_allow_html=True)


def setInputFocus():
    unique_id = random.randint(1, 10000)
    html_code = f"""
        <div style="display: none">
            <script key="{unique_id}">
                setTimeout(() => {{
                    const input = window.parent.document.querySelectorAll(
                        'textarea[data-testid=stChatInputTextArea]')[0];
                    if (input) {{
                        input.focus();
                    }}
                }}, 300);
            </script>
        </div>
        """
    with st.sidebar.container():
        st.components.v1.html(html_code, height=0)


def model_changed():
    model = st.session_state.get('selected_model', '')
    if 'last_selected_model' not in st.session_state or \
            st.session_state.last_selected_model != model:
        st.session_state.last_selected_model = model
        st.session_state.messages = [
            {"role": "assistant", "content": "您选择的模型是：" + model}
        ]
        setInputFocus()


def chat_bot():
    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.write(message["content"])
    if prompt := st.chat_input(placeholder="请输入您的问题", key="chat_input"):
        st.session_state.messages.append({"role": "user", "content": prompt})
        with st.chat_message("user"):
            st.markdown(prompt)
        model = st.session_state.get('selected_model', 'glm4')
        if st.session_state.messages[-1]["role"] != "assistant":
            with st.chat_message("assistant"):
                stream = client.chat.completions.create(
                    model=model,
                    messages=[
                        {"role": m["role"], "content": m["content"]}
                        for m in st.session_state.messages
                    ],
                    stream=True,
                )
                response = st.write_stream(stream)
                st.session_state.messages.append(
                    {"role": "assistant", "content": response}
                )


if __name__ == '__main__':
    init_page()
    init_sidebar()
    model_changed()
    chat_bot()
