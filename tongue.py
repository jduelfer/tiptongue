from flask import Flask, request, render_template
import os
import ling
app = Flask(__name__)


@app.route('/')
def intro():
    title = "Tip of the Tongue"
    return render_template('index.html', title=title)

@app.route('/', methods=['POST'])
def handle_input():
    text = request.form['text']
    processed_text = text.lower()
    tagged = ling.tag_input(processed_text)
    length = len(tagged)
    results = ling.collect_data(tagged, ling.data)
    freqs = ling.count_frequencies(results, length)
    organized_freqs = ling.organize_freqs(freqs)
    joined = ling.join_collected(results)
    revers = organized_freqs[:]
    revers.reverse()
    az = ling.alpha_freqs(organized_freqs)
    return render_template('display.html', tagged=tagged, processed_text=processed_text, results=results, organized_freqs=organized_freqs, joined=joined, revers=revers, az=az)
    

@app.route('/display/')
def display():
    return render_template('display.html')


if __name__ == "__main__":
    app.run()
    
