import DotaTrivia
from flask import Flask, render_template, request, jsonify, session
app = Flask(__name__)

@app.route('/')
def trivia():
    hero_info, hero_name = DotaTrivia.random_trivia()
    return render_template("index.html", hero_info = hero_info.replace("\n","<br>"), hero_name = hero_name)
if __name__ == '__main__':
    app.run(debug = True)#host = '0.0.0.0')
