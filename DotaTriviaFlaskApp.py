import DotaTrivia
from flask import Flask, render_template, request, jsonify, session
app = Flask(__name__)

@app.route('/')
def trivia():
    return DotaTrivia.random_trivia().replace('\n', '<br>')

if __name__ == '__main__':
    app.run(debug = True)#host = '0.0.0.0')
