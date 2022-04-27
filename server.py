from flask import Flask, render_template
from flask_restful import Api

app = Flask(__name__)
app.config['SECRET_KEY'] = 'secretkey?'
api = Api(app)


@app.route('/')
def main_page():
    return render_template("index.html", title="Главная страница")
