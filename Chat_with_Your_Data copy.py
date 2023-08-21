import streamlit as st
import openai
import os
import json
import requests
import openai

from azure.search.documents import SearchClient
import streamlit as st
from PIL import Image



openai.api_type = "azure"
openai.api_base = "https://*.openai.azure.com/" #fill in your Azure OpenAI instance
openai.api_version = "2023-03-15-preview"
openai.api_key = "" 


#Cognitive Search Connection
search_endpoint = "https://*.search.windows.net" #Use your Cog search name where * is
search_endpoint_for_creating_index = "https://*.search.windows.net/indexes/purview-vector-index/docs/search?api-version=2023-07-01-Preview" #Use your Cog search name where * is
search_api_key ="" #Cog search admin key
openai_api_key = openai.api_key

def createSearchRequest(user_question):
#Create an embedding for the user question
    response = openai.Embedding.create(
        input=user_question,
        engine="dh-embeddings-ada-002" #name of your embedding deployment
    )
    embeddings = response['data'][0]['embedding']

    #This is the search that will be sent to Azure Cog search in JSON format
    search_json = {
        "vector": {
            "value": embeddings,
            "fields": "contentVector, titleVector",
            "k": 2
        },
        "search": f"{user_question}",
        "select": "title, content, path",
        "queryType": "semantic",
        "semanticConfiguration": "my-semantic-config",
        "queryLanguage": "en-us",
        "captions": "extractive",
        "answers": "extractive",
        "top": "2"
    }

  
    url = f'{search_endpoint_for_creating_index }'
    print("")
    print("URL is " + url)
    headers = {'Content-Type': 'application/json', 'api-key': search_api_key}
    print("Search api key is " +search_api_key)
    #print("Search JSON is " + json.dumps(search_json))
    print("About to make the rest call")
    #print("data is" + str(search_json))
    response = requests.post(url , headers=headers, data=json.dumps(search_json))

    if response.status_code == 200:
        data = response.json()
        #print(data)
    else:
        print('Error:', response.status_code)       

    print("rest call completed") 

    array_length = len(data['value'])
    print("array length is " +str(array_length))
  

    #This gets the response from Azure Cognitive Search and puts it into variables
    azure_search_response = data['value'][0]['content']
    response_message = data['value'][0]['content']
    response_link = data['value'][0]['path']
    response_title = data['value'][0]['title']

    azure_search_response += data['value'][1]['content'] #This ensures we get the first two search results to feed to Azure OpenAI for the answer. Add more results if needed to improve response.
    print(azure_search_response)

    #This calls Azure OpenAI with the question and the search results to find an answer.
    addon_command = " Don't answer the question if you can't answer it using the text in the system message, just say 'I'm sorry, I don't have the answer to that question, can you please rephrase it?\" Don't say anything more after that."
    response = openai.ChatCompletion.create(
    engine="gpt-35-turbo-16k",
    messages = [{
            "role": "system",
            "content": f"You are an IT helpdesk bot. Try to answer the question based on the text that is given to you. Include all relevant information from the text. Text to look for an answer: {azure_search_response} "
        },
        {
            "role": "user",
            "content": user_question + addon_command
    }],
    temperature=0.2,
    max_tokens=8000,
    top_p=0.95,
    frequency_penalty=0,
    presence_penalty=0,
    stream=False,
    stop=None)

    print("=======\n\n")


    
    return response, response_message, response_title, response_link



st.title("🔎 Azure OpenAI Chat on Your Data")



st.write("<p style='text-align:center'>Put your sub-title here", unsafe_allow_html=True)

with st.form("my_form"):
    input_message = st.text_input('Question')
    submitted = st.form_submit_button("Submit")
    if submitted:
        response, response_message, response_title, response_link = createSearchRequest(input_message)
        #This prints out the Azure OpenAI response to the question
        st.write(response['choices'][0]['message']['content'])
        response_content = response['choices'][0]['message']['content']
        #st.write(response_message)
        #This section prints out a link to the first document in the search results if an answer was found
        substring = "I'm sorry"
        if substring not in str(response_content): 
            st.write("Source: <a href=" + response_link+ "> " +response_title +" </a>", unsafe_allow_html=True)












