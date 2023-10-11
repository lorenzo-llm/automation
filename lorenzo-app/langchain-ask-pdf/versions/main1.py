import os
import sys 
import pandas as pd
import constants
from langchain.llms import OpenAI
from langchain.chat_models import ChatOpenAI
from dotenv import load_dotenv
import streamlit as st
from langchain.document_loaders import TextLoader
from langchain.indexes import VectorstoreIndexCreator
from langchain.agents.agent_toolkits import FileManagementToolkit
from langchain.tools.file_management import (
    ReadFileTool,
    CopyFileTool,
    DeleteFileTool,
    MoveFileTool,
    WriteFileTool,
    ListDirectoryTool,
) 

tools = FileManagementToolkit(
    root_dir=str('/Users/vladimirbarshchuk/Downloads/'),
    selected_tools=["read_file", "write_file", "list_directory"],
).get_tools()
read_tool, write_tool, list_tool = tools

def main():
    load_dotenv()
    st.set_page_config(page_title="File Business Agent 📋",page_icon=None)
    st.header("Ask Your File Business Agent for Help 📋")
    st.text(body="Hey There ! \nWelcome to your free Business Agent 🤗 \nOur Business agent can handle various tasks such as: \n\n>Financial statements analysis 👨🏻‍💻 \n>Financial statements creation 🏛️ \n>Data wrangling 📊 \n>And SO MUCH MORE...\n\nTry This Prompt : Generate Income Statement based on this \ntrial balance infomration, add Tax Income Tax Expense of 10%.")
    title = st.text_input('Your Directory Path (in .txt):', placeholder="/Users/yourname/Directory/file.txt")
    
    if title is not None:
      query = st.text_input("What do you need help with ?", placeholder="Generate Income Statement Based on My Trial Balance")
      file_name = st.text_input("What would be output file name?", placeholder="IncomeStatement.txt")
      try:
        loader = TextLoader(title)
        index = VectorstoreIndexCreator().from_loaders([loader])
      except RuntimeError as error:
            print("Please Upload Your file!")

    if query is not None and query != "":
        response = str(index.query(query, llm=ChatOpenAI()))
        st.write(response)
        
    if st.button("Download Response", type="primary"):
       st.write("wait ~2 min for download to complete...")
       write_tool.run({"file_path":file_name, "text": response})
       
    hide_streamlit_style = """
            <style>
            #MainMenu {visibility: hidden;}
            footer {visibility: hidden;}
            </style>
            """
    st.markdown(hide_streamlit_style, unsafe_allow_html=True) 
if __name__ == '__main__':
    main()





