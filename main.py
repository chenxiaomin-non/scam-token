from unicodedata import name
import get_info, crawl_event, get_score, data, crawl_info

from flask import Flask, render_template, request

app = Flask(__name__)

@app.route('/')
def index():
    return render_template("index.html", notify="")

@app.route('/', methods=['POST'])
def response():
    # get input from request
    token_input = request.form['token']
    token_input = str(token_input).strip()

    # check validate of the input
    if token_input == '':
        notify = "The input string is invalid token"
        return render_template("index.html", notify=notify)
    else:
        check_validate = get_info.check_validate_input(token_input)
        if check_validate == 0:
            notify = "The input string is invalid token"
            return render_template("index.html", notify=notify)

    # process the input 
    # first, if the token already exists in database, retrieve it
    # else request to api 
    find_token_data = data.find_token_data(token_input)
    if  find_token_data == None:
        score, result, explain, name, symbol = get_score.get_score(token_input)
        if score >= 70:
            color = "springgreen"
        elif score >= 40:
            color = "orange"
        else:
            color = "red"    
        
        if score < 0:
            score = 0
        name, symbol, _ = crawl_info.get_info_from_BSC(token_input)
        data.insert_token_data(token_input, score, explain, result, color, name, symbol)
    else :
        _, score, explain, result, color, name, symbol = find_token_data

    

    return render_template("result.html", score=score, explain=explain.split('\n'), notify=result, color=color, name=name, symbol=symbol)

if __name__ == '__main__':
    app.run(debug=True)