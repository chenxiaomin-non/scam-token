import get_info, crawl_event, get_score

from flask import Flask, render_template

app = Flask(__name__)

@app.route('/')
def index():
    return render_template("index.html")

@app.route('/', methods=['POST'])
def response():
    score, explain = get_score.get_score()
    
    return render_template("result.html", score=score, explain=explain)

if __name__ == '__main__':
    app.run(debug=True)