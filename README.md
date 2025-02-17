# LangChain: Chat with SQL Database

### Overview

This Streamlit application allows users to interact with a SQL database using natural language queries. The app supports both SQLite and MySQL databases and leverages LangChain's SQL Agent with ChatGroq models for query processing.

### Features

- Database Selection: Choose between SQLite and MySQL databases.

- ChatGroq Models: Select from multiple LLM models including Llama3-8b-8192, Llama3-70b-8192, llama-3.3-70b-versatile, and Gemma2-9b-it.

- Interactive Chat: Query the database using natural language.

- Conversation History: Maintains chat history for better context.

- Error Handling: Displays relevant messages for missing inputs.

### Requirements

- Python 3.8+
- Streamlit
- LangChain
- SQLAlchemy
- SQLite3 or MySQL
- langchain_groq
- MySQL Connector (if using MySQL)

### Installation

Clone this repository:
```
git clone https://github.com/soopertramp/chat_with_database.git

cd chat-sql-langchain
```
### Install dependencies:

```pip install -r requirements.txt```

### Usage

#### Run the Streamlit app:

```streamlit run app.py```

- Configure the database and select a model from the sidebar.

- Enter queries in the chat box and get responses from the database.

### Configuration

- SQLite: Uses student.db (read-only mode).

- MySQL: Requires host, user, password, and database details.

- API Key: Provide a valid Groq API Key in the sidebar.

### Troubleshooting

- If using MySQL, ensure the database credentials are correct.

- Check that your Groq API key is valid.

- Ensure all required Python packages are installed.

### License

This project is licensed under the MIT License.

### Credits
This project is built using LangChain and integrates various AI tools for querying the database.
