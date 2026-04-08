import streamlit as st
import openai
from IPython.core.debugger import prompt
from streamlit import session_state


st.title("聊天机器人")
openai.api_key = "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"
openai.api_base = "https://openrouter.ai/api/v1"
if "openai_model" not in session_state:
    st.session_state["openai_model"]= "gpt-3.5-turbo"

if "openai_model" not in session_state:
    st.session_state.messages = []

if "messages" not in st.session_state:
    st.session_state.messages = []

if "prompts" not in st.session_state:
    st.session_state['prompts'] = []

def generate_response(prompt):
    st.session_state['prompts'].append({"role": "user", "content": prompt})
    completion = openai.ChatCompletion.create(
        model=st.session_state["openai_model"],
        messages=st.session_state['prompts']
    )
    message = completion.choices[0].message.content
    return message

if prompt := st.chat_input("有什么问题想问我？"):
    st.session_state.messages.append({"role":"user","content":prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    with st.chat_message("assistant"):
        message_placeholder = st.empty()
        full_response = generate_response(prompt)
        for response in openai.ChatCompletion.create(
            model = st.session_state["openai_model"],
            messages = [
                {"role" : m["role"],"content" : m["content"]}
                for m in st.session_state.messages
            ],
            stream = True
        ):

            for chunk in response :
                full_response += response.choices[0].delta.get("content","")
            message_placeholder.markdown(full_response)
    st.session_state.messages.append({"role":"assistant","content":full_response})