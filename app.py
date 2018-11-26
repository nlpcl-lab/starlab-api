import os, sys, datetime, random, json, requests
from flask import Flask, session, g, request, jsonify, render_template, redirect, Response
from flask_mongoengine import MongoEngine
from subprocess import Popen, PIPE

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


# All APIs

# artext
@app.route('/artext')
def artext_view():
    return render_template('api_artext.html')


from artext import Artext
artxt = Artext()
artxt.samples = 10
artxt.error_overall = 0.25

@app.route('/api/artext/noise', methods=['POST'])
def api_artext():
    log_api_access('artext')

    data = request.get_json()
    doc = data['input']
    noises = artxt.noise_document(doc)

    response = jsonify({'input': doc, 'output': '\n'.join(noises)})
    return response


# paraphrase
@app.route('/paraphraser')
def paraphrase_view():
    return render_template('api_paraphraser.html')

paraphraser_dir_path = '/home/webmaster/Web_API/API/Paraphrase_Generator'
paraphraser_args = [
    '{}/Paraphrase/moses'.format(paraphraser_dir_path), '-f',
    '{}/Working/mert-work/moses.ini'.format(paraphraser_dir_path),
    '-n-best-list',
    '2',
]
paraphraser_proc = Popen(paraphraser_args, stdin=PIPE, stdout=PIPE, stderr=PIPE)
@app.route('/api/paraphraser', methods=['POST'])
def api_paraphraser():
    log_api_access('paraphraser')
    data = request.get_json()
    sentence = data['input'] + '\n'
    paraphraser_proc.stdin.write(sentence.encode())
    paraphraser_proc.stdin.flush()
    result = paraphraser_proc.stdout.readline().decode()
    result = result.replace('\n', '')

    response = jsonify({'input': sentence, 'output': result})
    return response


# summarize
@app.route('/summarization')
def summarize_view():
    return render_template('api_summarization.html')


@app.route('/api/summarization', methods=['POST'])
def summarization_process():
    log_api_access('summarization')

    data = request.get_json()
    sentence = data['input']

    # TODO: Implement Operation Here
    summary = sentence

    response = jsonify({'input': sentence, 'output': summary})
    return response


# event-extraction
@app.route('/event-extraction')
def event_extraction_view():
    return render_template('api_event_extraction.html')


@app.route('/api/event-extraction', methods=['POST'])
def api_event_extraction():
    log_api_access('event-extraction')
    data = request.get_json()
    sentence = data['input']

    res = requests.post('http://credon.kaist.ac.kr:8085/api/event-extraction/trigger/identification', json={
     'sentence': sentence,
    })
    output = res.json()['result']
    response = jsonify({'input': sentence, 'output': output})
    return response


# monolingual-sentence-aligner
@app.route('/monolingual-sentence-aligner')
def sentence_aligner_view():
    return render_template('api_sentence_aligner.html')


@app.route('/api/monolingual-sentence-aligner', methods=['POST'])
def api_sentence_aligner():
    log_api_access('monolingual-sentence-aligner')

    data = request.get_json()
    input_1 = data['input_1']
    input_2 = data['input_2']

    # TODO: Implement Operation Here
    output = input_1 + input_2

    response = jsonify({'input_1': input_1, 'input_2': input_2, 'output': output})
    return response


# automatic-tension-detection
@app.route('/automatic-tension-detection')
def tension_detection_view():

    return render_template('api_tension_detection.html')


@app.route('/api/automatic-tension-detection', methods=['POST'])
def api_tension_detection():
    log_api_access('automatic-tension-detection')
    data = request.get_json()
    sentence = data['input']
    res = requests.post('http://credon.kaist.ac.kr:8086/api/tension-detection', json={
        'input': sentence,
    })
    output = res.json()['output']
    response = jsonify({'input': sentence, 'output': output})
    return response


# context-dependent-evidence-detection
@app.route('/context-dependent-evidence-detection')
def evidence_detection_view():
    return render_template('api_evidence_detection.html')


@app.route('/api/context-dependent-evidence-detection', methods=['POST'])
def api_evidence_detection():
    log_api_access('context-dependent-evidence-detection')

    data = request.get_json()
    sentence = data['input']

    # TODO: Implement Operation Here
    output = sentence

    response = jsonify({'input': sentence, 'output': output})
    return response


# argument-reasoning-comprehension
@app.route('/argument-reasoning-comprehension')
def argument_comprehension_view():
    return render_template('api_argument_comprehension.html')


@app.route('/api/argument-reasoning-comprehension', methods=['POST'])
def api_argument_comprehension():
    log_api_access('argument-reasoning-comprehension')

    data = request.get_json()
    sentence = data['input']

    # TODO: Implement Operation Here
    output = sentence

    response = jsonify({'input': sentence, 'output': output})
    return response


if __name__ == '__main__':
    base_dir = os.path.abspath(os.path.dirname(__file__) + '/')
    sys.path.append(base_dir)

    app.secret_key = config.Config.SECRET_KEY
    FLASK_DEBUG = os.getenv('FLASK_DEBUG', False)
    app.run(host='0.0.0.0', debug=FLASK_DEBUG, port=8084)
