import get_info, crawl_event, get_score

from flask import Flask, render_template, request

app = Flask(__name__)

@app.route('/')
def index():
    return render_template("index.html")

@app.route('/', methods=['POST'])
def response():
    token_input = request.form['token']
    token_input = str(token_input)

    score, explain = get_score.get_score(token_input)
    
    return render_template("result.html", score=score, explain=explain)

if __name__ == '__main__':
    app.run(debug=True)