from flask import Flask, request, jsonify
import json
import pandas as pd
from transformers import pipeline
import nltk
from keybert import KeyBERT
from nltk import tokenize

nltk.download('punkt')
app = Flask(__name__)
summarizer = pipeline("summarization", model="facebook/bart-large-cnn")

@app.route("/")
def hello_world():
    return "<p>Hello, World!</p>"


@app.route('/domachinelearningstuff', methods=['POST'])
def domachinelearningstuff():
    jason = request.json
    transcript_df = pd.read_json(json.dumps(jason), orient="records")
    text = transcript_df.text.str.cat(sep='')

    sentences = tokenize.sent_tokenize(text)

    chunks = [sentences[x:x+10] for x in range(0, len(sentences), 10)]

    for i in range(len(chunks)):
        chunks[i]= " ".join(chunks[i])
    for i in range(len(chunks)):
        print("gang")
        chunks[i] = summarizer(chunks[i], max_length=130, min_length=5)
    summary_list = []
    for chunk in chunks:
        summary_list.append(chunk[0]['summary_text'])    
    summarized = ''.join(summary_list)
    model = KeyBERT(model="distilbert-base-nli-mean-tokens")
    out=model.extract_keywords(
        summarized,
        top_n=10,
        keyphrase_ngram_range=(1, 1),
        stop_words="english",
    )
    topics = []
    for item in out:
        topics.append(item[0])
    output = {
        "topics": topics,
        "summarized_rows": summary_list
    }
    return json.dumps(output)

