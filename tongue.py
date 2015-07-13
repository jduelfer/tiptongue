from flask import Flask, request, render_template
import os
import ling
import logging
import sys
import nltk

root = logging.getLogger()
root.setLevel(logging.DEBUG)

ch = logging.StreamHandler(sys.stdout)
ch.setLevel(logging.DEBUG)
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
ch.setFormatter(formatter)
root.addHandler(ch)

app = Flask(__name__)


@app.route('/')
def intro():
    title = "Tip of the Tongue"
    return render_template('index.html', title=title)

@app.route('/', methods=['GET','POST'])
def handle_input():
    text = request.form['text']
    processed_text = text.lower()
    try:
        tagged = ling.tag_input(processed_text)
    except LookupError:
        nltk.download()
        nltk.download('punkt')
        tagged = ling.tag_input(processed_text)
    length = len(tagged)
    results = ling.collect_data(tagged, ling.data)
    freqs = ling.count_frequencies(results, length)
    organized_freqs = ling.organize_freqs(freqs)
    joined = ling.join_collected(results)
    revers = organized_freqs[:]
    revers.reverse()
    az = ling.alpha_freqs(organized_freqs)
    ##return render_template('display.html', tagged=tagged, processed_text=processed_text, results=results, organized_freqs=organized_freqs, joined=joined, revers=revers, az=az)
    return display(tagged, processed_text, results, organized_freqs, joined, revers, az)
    

@app.route('/display/')
def display(tagged, processed_text, results, organized_freqs, joined, revers, az):
    return render_template('display.html', tagged=tagged, processed_text=processed_text, results=results, organized_freqs=organized_freqs, joined=joined, revers=revers, az=az)


if __name__ == "__main__":
    app.run()
    
