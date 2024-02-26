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
    
#curl 'http://192.168.1.10:5000/chatresponse' -d 'prompt=What is mental health?'
if __name__ == '__main__':
    app.run(host='0.0.0.0',port=5000)