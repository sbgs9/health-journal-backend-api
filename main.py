from flask import Flask, jsonify, request
from huggingface_hub import InferenceClient
import os
from dotenv import load_dotenv
#import nltk
from nltk import tokenize

load_dotenv()
app = Flask(__name__)
# RUN THE COMMENTED LINE BELOW WHEN RUNNING FOR THE FIRST TIME
#nltk.download('punkt')
client = InferenceClient(model='mistralai/Mistral-7B-Instruct-v0.2', token=os.environ.get("HUGGINGFACE_TOKEN"))
@app.route('/chatresponse', methods=['POST'])
def chat_response():
    prompt = request.form.get('prompt')
    data = client.text_generation(max_new_tokens=100, prompt=prompt)
    tokenized_data = tokenize.sent_tokenize(data)
    last_sentence = tokenized_data[-1]
    if last_sentence[-1] == '?' or last_sentence[-1] != '.' or last_sentence[-1] != '!':
        tokenized_data = tokenized_data[:len(tokenized_data) - 1]
    chat_response = " ".join(sentence for sentence in tokenized_data)
    return jsonify({'chat_response': chat_response})

@app.route('/userintent', methods=['POST'])
def user_intent():
    system_prompt = """You are a mental health assistant. 
    
    You are supposed to understand the user's query and classify it into one of three possible actions based on what the user wants to do. The three possible actions are the following: chat with a chatbot, search for resources, and book an appointment. 
    
    An example for the "chat with a chatbot" option would be if a user asked a question, such as "What is mental health?" or "What is depression?" 
    
    An example for the "search for resources" option would be if a user said "can you give me resources for depression?" 
    
    An example for the "book an appointment" option would be if a user said "I would like to book an appointment", or "Can I book an appointment?". 

    Based on the user's query, respond with one of those three possible choices in the following format:
    
    user_intent:CHAT_WITH_CHATBOT
    user_intent:SEARCH_FOR_RESOURCES
    user_intent:BOOK_APPOINTMENT
    
    In the above format, respond to the user's query."""
    prompt = request.form.get('prompt')
    final_prompt = system_prompt + prompt
    data = client.text_generation(prompt=final_prompt)
    return jsonify({'user_intent': data})
    
#curl 'http://192.168.1.10:5000/userintent' -d 'prompt=What is mental health?'
if __name__ == '__main__':
    app.run(host='0.0.0.0',port=5000)