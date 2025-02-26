import sys
from openai import AzureOpenAI
import time 
import os 
from datetime import datetime
from dotenv import load_dotenv
import json

current_date = datetime.now().date()

sys.stdout.reconfigure(encoding='utf-8')

load_dotenv()



input_data_path = "./staging/data_" +  str(current_date) +".json"
parent_dir = "./data/"
Sys_Prompt_path = './prompts/SysPrompt.txt'
User_Prompt_path = './prompts/UserPrompt.txt'


AZURE_OPENAI_API_KEY = os.getenv('AZURE_OPENAI_API_KEY')
AZURE_OPENAI_API_ENDPOINT = os.getenv("AZURE_OPENAI_API_ENDPOINT")

def sanitize(text):
    for t in text :
        if not t :
            text.replace(t,'')
    return text.strip()

with open(input_data_path, 'r',encoding='utf-8') as f :
    data = json.load(f)
    for i in range (len(data)):
        data[i]['Content'] = sanitize(data[i]['Content'])


client = AzureOpenAI(
    api_key= AZURE_OPENAI_API_KEY,
    azure_endpoint=AZURE_OPENAI_API_ENDPOINT,
    api_version= "2024-02-01",
)


with open(Sys_Prompt_path,'r',encoding= 'utf-8') as f :
    sys_prompt = f.read()

with open(User_Prompt_path, 'r') as f :
    user_prompt = f.read()



def load_to_txt(parent_dir, processed_new,title):
    
    output_data_path = parent_dir + f"{str(current_date)}" + "-"  + f"{title}" + ".txt"    
    with open(output_data_path,'w',encoding= 'utf8') as f :
        f.write(processed_new)

def load_to_json(output_data_path, processed_news) : 
    
    with open(output_data_path, 'r' , encoding = 'utf8') as f :
        data = json.load(f)
    data  = data + processed_news
    with open(output_data_path, 'w', encoding='utf8') as f:
        json.dump(data, f, indent = 2, ensure_ascii= False)


for i in range (len(data)):
    
    time.sleep(5)
    
    response = client.chat.completions.create(
        model="chat-gpt-4o",
        messages=[
            {
                "role": "system",
                "content": [
                    {
                    "type": "text",
                    "text": f"{sys_prompt}"
                    }
                ]
            },
            {
                "role": "user",
                "content": [
                    {
                    "type": "text",
                    "text": f"Use the following text as input and follow the instruction:\n {data[i]['Title']} \n {data[i]['Content']}"
                    }
                ]
            }
        ]
    )

    load_to_txt(parent_dir,response.choices[0].message.content, data[i]['Title'])
    
