import streamlit as st
from io import StringIO
import sys
import os 
import json
sys.stdout.reconfigure(encoding='utf-8')

web_config_file_path =  "./airflow/web_crawler/crawler.json"
sys_prompt_file_path = "./prompts/SysPrompt.txt"
file_parent_dir =  "./data"

with open(web_config_file_path,'r') as f:
    config = json.load(f)

with open(sys_prompt_file_path,'r', encoding= 'utf-8') as f :
    sys_prompt = f.read()

st.sidebar.header("Choose landing page")
option = st.sidebar.radio("Options" , ["Show currnet setting", "Change current setting" , "Show processed files"])


def show_cur_setting() : 
    st.title("Current Web config")
    st.json(config)
    
    st.title("Current prompt config")
    st.text(sys_prompt)
    
def change_cur_setting():
    st.header("Upload web config file here")
    web_config_file = st.file_uploader(label='Web Config',accept_multiple_files=False)

    st.header("Upload prompt file here")
    sys_prompt_file = st.file_uploader(label='Prompt',accept_multiple_files=False)

    button1 = st.button('Press to update changes')



    if button1 :
        if web_config_file is not None:
            web_config = web_config_file.getvalue()
            with open(web_config_file_path, 'wb') as f :
                f.write(web_config)

        if sys_prompt_file is not None:
            sys_prompt = sys_prompt_file.getvalue()
            with open(sys_prompt_file_path, 'wb') as f :
                f.write(sys_prompt)
        st.write("Changes have been made successfully")


def show_files():
    files = os.listdir(file_parent_dir)
    files.sort()
    file = st.selectbox("Choose a file" , files)
    if file : 
        with open(file_parent_dir + "/" +file,encoding= 'utf-8') as f :
            content = f.read()
        st.title("File content")
        st.text(content)

def main():
    
    if option == "Show currnet setting":
        show_cur_setting()
    elif option == "Change current setting":
        change_cur_setting()
    elif option == "Show processed files":
        show_files()
if __name__ == "__main__" :
    main()
