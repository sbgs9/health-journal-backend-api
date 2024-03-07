from flask import Flask, Response, request, jsonify
import time
import json
import threading
from flask import Flask, request, jsonify
from urllib.parse import urlparse
import requests
import re
from urlValidatorFun import *
from crawlers import *
from resources import *
from bs4 import BeautifulSoup
import validators

app = Flask(__name__)

data_queue = []
pdf_queue = []
work_flag = threading.Event()
work_flag.set()  # Set the event initially to True


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

@app.route('/process_query', methods=['POST'])
def process_query_endpoint():
    global work_flag
    work_flag.set() # setting the flag
    query = request.json['query']
    process_query_thread(query)
    #work_flag.clear()  # Clear the event to False to indicate processing
    return jsonify({"message": "Processing query..."})

@app.route('/events')
def events():
    global work_flag
    work_flag.wait()  # Wait until the event is set (True)
    while work_flag.is_set() or data_queue:
        if data_queue:
            yield f"data: {json.dumps(data_queue.pop(0))}\n\n"
        time.sleep(1)
    yield "event: end"

if __name__ == '__main__':
    app.run(debug=True)
