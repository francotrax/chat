# import streamlit as st
# import openai
# import os

# from dotenv import load_dotenv

# openai.api_key = os.environ["OPENAI_API_KEY"]

# st.title("Yazo Chat")

# if "messages" not in st.session_state:
#     st.session_state.messages = []

# for message in st.session_state["messages"]:
#     with st.chat_message(message["role"]):
#         st.markdown(message["content"])

# # Initialize model
# if user_prompt := st.chat_input("Your prompt"):
#     st.session_state.messages.append({"role": "user", "content": user_prompt})
#     with st.chat_message("user"):
#         st.markdown(user_prompt)

#     # generate responses
#     with st.chat_message("assistant"):
#         message_placeholder = st.empty()
#         full_response = ""

#         for response in openai.ChatCompletion.create(
#             model=st.session_state.model,
#             messages=[
#                 {"role": m["role"], "content": m["content"]}
#                 for m in st.session_state.messages
#             ],
#             stream=True,
#         ):
#             full_response += response.choices[0].delta.get("content", "")
#             message_placeholder.markdown(full_response + "▌")

#         message_placeholder.markdown(full_response)

#     st.session_state.messages.append({"role": "assistant", "content": full_response})


import os
import streamlit as st
from dotenv import load_dotenv
from langchain.llms import OpenAI
from langchain.agents import AgentType, initialize_agent, load_tools
from langchain.callbacks import StreamlitCallbackHandler

# Initialize environment variables
load_dotenv()

# Initialize LLM
llm = OpenAI(temperature=0, streaming=True, openai_api_key=os.getenv("OPENAI_API_KEY"))
tools = load_tools(["ddg-search"])
agent = initialize_agent(
    tools,
    llm,
    agent=AgentType.ZERO_SHOT_REACT_DESCRIPTION,
    # verbose=True
)

# Title
st.title("Yazo Chat123")

for message in st.session_state["messages"]:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# Main logic
if "messages" not in st.session_state:
    st.session_state.messages = []



# try: "what are the names of the kids of the 44th president of america"
# try: "top 3 largest shareholders of nvidia"
if user_prompt := st.chat_input("Your prompt"):
    st.session_state.messages.append({"role": "user", "content": user_prompt})
    
    st.chat_message("user").write(user_prompt)
    with st.chat_message("assistant"):
        st.write("🧠 thinking...")
        st_callback = StreamlitCallbackHandler(st.container())
        response = agent.run(user_prompt, callbacks=[st_callback])
        st.write(response)