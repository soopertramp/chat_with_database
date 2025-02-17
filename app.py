import streamlit as st
from pathlib import Path
from langchain.agents import create_sql_agent
from langchain.sql_database import SQLDatabase
from langchain.agents.agent_types import AgentType
from langchain.callbacks import StreamlitCallbackHandler
from langchain.agents.agent_toolkits import SQLDatabaseToolkit
from sqlalchemy import create_engine
import sqlite3
from langchain_groq import ChatGroq
import os
from dotenv import load_dotenv

load_dotenv()

## Langsmith Tracking
os.environ["LANGCHAIN_API_KEY"]=os.getenv("LANGCHAIN_API_KEY")
os.environ["LANGCHAIN_TRACING_V2"]="true"
os.environ["LANGCHAIN_PROJECT"]="Chat With Database"

# Set page configuration
st.set_page_config(page_title="Chat with SQL Database", page_icon="🛢️", layout="wide")
st.title("🛢️Chat with SQL Database")

# Database options
LOCALDB = "USE_LOCALDB"
MYSQL = "USE_MYSQL"

st.sidebar.header("Settings ⚙️")

# Database selection
db_option = st.sidebar.selectbox("Choose the DB to chat with:", ["Use Local Database - Student Table", "Connect to your MySQL Database"])

# MySQL Credentials
if db_option == "Connect to your MySQL Database":
    db_uri = "USE_MYSQL"
    mysql_host = st.sidebar.text_input("MySQL Host")
    mysql_user = st.sidebar.text_input("MySQL User")
    mysql_password = st.sidebar.text_input("MySQL Password", type="password")
    mysql_db = st.sidebar.text_input("MySQL Database")
else:
    db_uri = "USE_LOCALDB"

# Select model
model_name = st.sidebar.selectbox("Select ChatGroq Model:", ["Llama3-8b-8192", "Llama3-70b-8192", "llama-3.3-70b-versatile", "Gemma2-9b-it"])

# API Key input
api_key = st.sidebar.text_input("GRoq API Key", type="password")

# Error messages
if not db_uri:
    st.error("Please enter the database information.")
    st.stop()
if not api_key:
    st.error("Please add the Groq API key.")
    st.stop()

# LLM model
llm = ChatGroq(groq_api_key=api_key, model_name=model_name, streaming=True)

# Database configuration
@st.cache_resource(ttl="2h")
def configure_db(db_uri, mysql_host=None, mysql_user=None, mysql_password=None, mysql_db=None):
    if db_uri == LOCALDB:
        dbfilepath = (Path(__file__).parent / "student_info.db").absolute()
        creator = lambda: sqlite3.connect(f"file:{dbfilepath}?mode=ro", uri=True)
        return SQLDatabase(create_engine("sqlite:///", creator=creator))
    elif db_uri == MYSQL:
        if not (mysql_host and mysql_user and mysql_password and mysql_db):
            st.error("Please provide all MySQL connection details.")
            st.stop()
        return SQLDatabase(create_engine(f"mysql+mysqlconnector://{mysql_user}:{mysql_password}@{mysql_host}/{mysql_db}"))
    
if db_uri == MYSQL:
    db = configure_db(db_uri, mysql_host, mysql_user, mysql_password, mysql_db)
else:
    db = configure_db(db_uri)

# Toolkit
toolkit = SQLDatabaseToolkit(db=db, llm=llm)

# SQL Agent
agent = create_sql_agent(
    llm=llm,
    toolkit=toolkit,
    verbose=True,
    agent_type=AgentType.ZERO_SHOT_REACT_DESCRIPTION
)

# Conversation history
if "messages" not in st.session_state or st.sidebar.button("Clear Chat History"):
    st.session_state["messages"] = [{"role": "assistant", "content": "How can I assist you?"}]

for msg in st.session_state.messages:
    st.chat_message(msg["role"]).write(msg["content"])

# Credits section at the bottom of the sidebar
st.sidebar.markdown("---")
st.sidebar.markdown("**Powered by [LangChain](https://github.com/langchain-ai/streamlit-agent)**")

# User input
user_query = st.chat_input(placeholder="Ask anything from the database")

if user_query:
    st.session_state.messages.append({"role": "user", "content": user_query})
    st.chat_message("user").write(user_query)

    with st.chat_message("assistant"):
        streamlit_callback = StreamlitCallbackHandler(st.container())
        conversation_history = "\n".join([f"{msg['role']}: {msg['content']}" for msg in st.session_state.messages])
        response = agent.run(f"{conversation_history}\nUser: {user_query}", callbacks=[streamlit_callback])
        st.session_state.messages.append({"role": "assistant", "content": response})
        st.write(response)