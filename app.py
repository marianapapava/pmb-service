from flask import request, Flask, jsonify
from flask_cors import CORS

from model import *

import datetime as dt

app = Flask(__name__)
app.config.from_object(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:////tmp/test.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db.init_app(app)

CORS(app)

@app.cli.command('initdb')
def initdb():
    db.create_all()

@app.route('/spider/sedinte', methods=['POST'])
def update_sedinta():
    sedinta = request.get_json()
    sedinta['data'] = dt.datetime.strptime(sedinta['data'], '%Y-%m-%d, %H:%M')

    current_sedinta = Sedinta.query.all()
    if current_sedinta:
        if current_sedinta[0].data == sedinta['data']:
            return jsonify({'status': 'OK'})

        else:
            db.session.delete(current_sedinta[0])

    new_sedinta = Sedinta(sedinta['data'])
    db.session.add(new_sedinta)
    for item_sedinta in sedinta['itemuri']:
        db.session.add(ItemSedinta(
            new_sedinta,
            item_sedinta['descriere'],
            item_sedinta['url']
        ))

    db.session.commit()

    return jsonify({'status': 'OK'})

@app.route('/spider/dezbateri', methods=['POST'])
def update_dezbateri():
    body = request.get_json()

    Dezbatere.query.delete()

    for dezbatere in body:
        dezbatere['data_publicare'] = dt.datetime.strptime(dezbatere['data_publicare'], '%Y-%m-%d')
        dezbatere['termen_recomandari'] = dt.datetime.strptime(dezbatere['termen_recomandari'], '%Y-%m-%d')

        db.session.add(Dezbatere(
            dezbatere['numar_proiect'],
            dezbatere['data_publicare'],
            dezbatere['descriere'],
            dezbatere['url_document'],
            dezbatere['termen_recomandari'],
            dezbatere['imbunatatire'],
            dezbatere['imbunatatire_url']
        ))

    db.session.commit()

    return jsonify({'status': 'OK'})

@app.route('/app/sedinte', methods=['GET'])
def get_sedinte():
    sedinta = Sedinta.query.all()
    if not sedinta:
        return jsonify(sedinta)

    sedinta = sedinta[0]
    ret = {}
    ret['data'] = sedinta.data
    ret['itemuri'] = []
    for item_sedinta in sedinta.itemuri:
        ret['itemuri'].append({
            'descriere': item_sedinta.descriere,
            'url': item_sedinta.url
        })

    return jsonify(ret)

@app.route('/app/dezbateri', methods=['GET'])
def get_dezbateri():
    dezbateri = Dezbatere.query.all()
    if not dezbateri:
        return jsonify(dezbateri)

    ret = []
    for dezbatere in dezbateri:
        ret.append({
            'numar_proiect': dezbatere.numar_proiect,
            'data_publicare': dezbatere.data_publicare,
            'descriere': dezbatere.descriere,
            'url_document': dezbatere.url_document,
            'termen_recomandari': dezbatere.termen_recomandari,
            'imbunatatire': dezbatere.imbunatatire,
            'imbunatatire_url': dezbatere.imbunatatire_url
        })

    return jsonify(ret)
