import os
import utils
import streamlit as st
from dotenv import load_dotenv
from langchain.agents import AgentType
from langchain.chat_models import ChatOpenAI
from langchain.tools import DuckDuckGoSearchRun
from langchain.agents import initialize_agent, Tool
from langchain.callbacks import StreamlitCallbackHandler

# # Initialize environment variables
load_dotenv()

st.set_page_config(page_title="ChatWeb", page_icon="🌐")
st.header('Chatbot with Internet Access')
st.write('Equipped with internet access, enables users to ask questions about recent events')
st.write('[![view source code ](https://img.shields.io/badge/view_source_code-gray?logo=github)](https://github.com/shashankdeshpande/langchain-chatbot/blob/master/pages/3_%F0%9F%8C%90_chatbot_with_internet_access.py)')

# Sidebar
persona_selectbox = st.sidebar.selectbox(
    "Specify personality of AI chat bot.",
    ("General AI", "Translator", "Marketing Expert")
)

lang_input_selectbox = st.sidebar.selectbox(
    "Specify input language.",
    ("English", "Croatian")
)

lang_output_selectbox = st.sidebar.selectbox(
    "Specify output language.",
    ("English", "Croatian")
)

# Main
class ChatbotTools:

    def setup_agent(self):
        # Define tool
        ddg_search = DuckDuckGoSearchRun()
        tools = [
            Tool(
                name="DuckDuckGoSearch",
                func=ddg_search.run,
                description="Useful for when you need to answer questions about current events. You should ask targeted questions",
            )
        ]

        # Setup LLM and Agent
        llm = ChatOpenAI(model_name="gpt-3.5-turbo", streaming=True, openai_api_key=os.getenv("OPENAI_API_KEY"))
        agent = initialize_agent(
            tools=tools,
            llm=llm,
            agent=AgentType.ZERO_SHOT_REACT_DESCRIPTION,
            handle_parsing_errors=True,
            verbose=True
        )
        return agent

    @utils.enable_chat_history
    def main(self):
        agent = self.setup_agent()
        user_query = st.chat_input(max_chars=3000, placeholder="Ask me anything!")
        if user_query:
            utils.display_msg(user_query, 'user')
            with st.chat_message("assistant"):
                st_cb = StreamlitCallbackHandler(st.container())
                response = agent.run(user_query, callbacks=[st_cb])
                st.session_state.messages.append({"role": "assistant", "content": response})
                st.write(response)

if __name__ == "__main__":
    obj = ChatbotTools()
    obj.main()


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


# import os
# import streamlit as st
# from dotenv import load_dotenv
# from langchain.llms import OpenAI
# from langchain.agents import AgentType, initialize_agent, load_tools
# from langchain.callbacks import StreamlitCallbackHandler

# # Initialize environment variables
# load_dotenv()

# # Initialize LLM
# llm = OpenAI(temperature=0, streaming=True, openai_api_key=os.getenv("OPENAI_API_KEY"))
# tools = load_tools(["ddg-search"])
# agent = initialize_agent(
#     tools,
#     llm,
#     agent=AgentType.ZERO_SHOT_REACT_DESCRIPTION,
#     # verbose=True
# )

# # Title
# st.title("Yazo Chat")

# for message in st.session_state["messages"]:
#     with st.chat_message(message["role"]):
#         st.markdown(message["content"])

# # Main logic
# if "messages" not in st.session_state:
#     st.session_state.messages = []



# # try: "what are the names of the kids of the 44th president of america"
# # try: "top 3 largest shareholders of nvidia"
# if user_prompt := st.chat_input("Your prompt"):
#     st.session_state.messages.append({"role": "user", "content": user_prompt})
    
#     st.chat_message("user").write(user_prompt)
#     with st.chat_message("assistant"):
#         st.write("🧠 thinking...")
#         st_callback = StreamlitCallbackHandler(st.container())
#         response = agent.run(user_prompt, callbacks=[st_callback])
#         st.write(response)