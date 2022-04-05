from flask import Flask, request
from flask_restful import abort, Api

app = Flask(__name__)
app.config['SECRET_KEY'] = 'secretkey?'
api = Api(app)


# May be I'll add some api URLs
# api.add_resource()

@app.route('/')
def main_page():
    return "Hi"


if __name__ == '__main__':
    app.run()
