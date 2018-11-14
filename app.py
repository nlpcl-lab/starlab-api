import os, sys, datetime, random, json
from flask import Flask, session, g, request, jsonify, render_template, redirect, Response
from flask_mongoengine import MongoEngine

import config
from models import APIAccessLog



app = Flask(__name__)

app.config.from_object('config.Config')
db = MongoEngine(app)


@app.before_request
def before_request():
    if request.headers.getlist("X-Forwarded-For"):
        g.last_ip = request.headers.getlist("X-Forwarded-For")[0]
    else:
        g.last_ip = request.remote_addr


@app.route('/')
def index_view():
    with open('./apis.json') as f:
        apis = json.load(f)
        return render_template('index.html', apis=apis, APIAccessLog=APIAccessLog)


def log_api_access(key):
    log = APIAccessLog(key=key, ip=g.last_ip)
    log.save()



# APIs

# artext
@app.route('/artext')
def artext_view():
    return render_template('api_artext.html')


from artext import Artext
artxt = Artext()
artxt.samples = 10
artxt.error_overall = 0.25

@app.route('/api/artext/noise', methods=['POST'])
def artext_process():
    log_api_access('artext')

    data = request.get_json()
    doc = data['input']
    noises = artxt.noise_document(doc)

    response = jsonify({'input': doc, 'output': '\n'.join(noises)})
    return response


if __name__ == '__main__':
    base_dir = os.path.abspath(os.path.dirname(__file__) + '/')
    sys.path.append(base_dir)

    app.secret_key = config.Config.SECRET_KEY
    FLASK_DEBUG = os.getenv('FLASK_DEBUG', False)
    app.run(host='0.0.0.0', debug=FLASK_DEBUG, port=8084)
