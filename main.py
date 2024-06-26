from flask import Flask, jsonify, request, Response
from flask_cors import CORS
from huggingface_hub import InferenceClient
import os
from dotenv import load_dotenv
#import nltk
from nltk import tokenize
import time
import json
import threading
import requests
from urlValidatorFun import *
from crawlers import *
from resources import *

load_dotenv()
app = Flask(__name__)
CORS(app)
data_queue = []
pdf_queue = []
work_flag = threading.Event()
work_flag.set()  # Set the event initially to True
chat_client = InferenceClient(model='mistralai/Mistral-7B-Instruct-v0.2', token=os.environ.get("HUGGINGFACE_TOKEN"))
intent_client = InferenceClient(model='facebook/bart-large-mnli', token=os.environ.get("HUGGINGFACE_TOKEN"))

def getCredentials():
    api_key = 'AIzaSyCf4Xi9YgFeGfhXS2PGx4f6ymvSFDV6AG0'
    cx = '11054718dc20742aa'
    return api_key, cx

def customSearchEngine(query,num_results=2):
    api_key, cx = getCredentials()

    url = f"https://www.googleapis.com/customsearch/v1?key={api_key}&cx={cx}&q={query}&num={num_results}"

    response = requests.get(url)
    if response.status_code == 200:
        results = response.json().get('items', [])
        urls = [result['link'] for result in results]
        return urls
    else:
        print("Error:", response.text)
        return []

def worker_logic(query):
    global data_queue

    result = customSearchEngine(query,num_results=10)
    data_queue.append({'search': result})

    for i in result:
        text = crawlerParagraph(i)
        x = crawlerPDF(i)
        if x:
            data_queue.append({'pdf': x})
        x = get_lines_with_proper_nouns_and_contacts(text)
        if x:
            data_queue.append({'contact': x})
        x = linkExtractor(text)
        if x:
            data_queue.append({'link': x})

    work_flag.clear() # ending the event after completing the working logic

# Function to process the query in a separate thread
def process_query_thread(query):
    worker_thread = threading.Thread(target=worker_logic, args=(query,))
    worker_thread.start()
# RUN THE COMMENTED LINE BELOW WHEN RUNNING FOR THE FIRST TIME
#nltk.download('punkt')

@app.route('/chatresponse', methods=['POST'])
def chat_response():
    prompt = request.form.get('prompt')
    data = chat_client.text_generation(max_new_tokens=100, prompt=prompt)
    tokenized_data = tokenize.sent_tokenize(data)
    last_sentence = tokenized_data[-1]
    if last_sentence[-1] == '?' or last_sentence[-1] != '.' or last_sentence[-1] != '!':
        tokenized_data = tokenized_data[:len(tokenized_data) - 1]
    chat_response = " ".join(sentence for sentence in tokenized_data)
    return jsonify({'chat_response': chat_response})

@app.route('/userintent', methods=['POST'])
def user_intent():
    labels = ['book appointment', 'view appointments','cancel appointment', 'question', 'chat', 'search for resources']
    prompt = request.form.get('prompt')
    data = intent_client.zero_shot_classification(prompt, labels)
    response = jsonify({'user_intent': data})
    return response

@app.route('/process_query', methods=['POST'])
def process_query_endpoint():
    global work_flag
    work_flag.set() # setting the flag
    query = request.json['query']
    result = customSearchEngine(query, num_results=10)
    #process_query_thread(query)
    #work_flag.clear()  # Clear the event to False to indicate processing
    return jsonify({"links": result})

# @app.route('/events')
# def events():
#     global work_flag
#     work_flag.wait()  # Wait until the event is set (True)
#     def generate():
#         global data_queue
#         while work_flag.is_set() or data_queue:
#             if data_queue:
#                 yield f"data: {json.dumps(data_queue.pop(0))}\n\n"
#             time.sleep(1)
#         yield "event: end"
#     return Response(generate(), content_type='text/event-stream')
    
#curl 'http://192.168.1.10:5000/userintent' -d 'prompt=What is mental health?'
if __name__ == '__main__':
    app.run(host='0.0.0.0',port=5000)