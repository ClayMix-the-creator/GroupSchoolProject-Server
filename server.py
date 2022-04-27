from flask import Flask, request, render_template
from flask_restful import abort, Api

app = Flask(__name__)
app.config['SECRET_KEY'] = 'secretkey?'
api = Api(app)


# Lol, I'm doing a server, not a website
# api.add_resource()

@app.route('/')
def main_page():
    return render_template("index.html", title="Главная страница")


if __name__ == '__main__':
    app.run()
