from flask_sqlalchemy import SQLAlchemy

from model.shared import db

class Dezbatere(db.Model):
    numar_proiect = db.Column(db.Integer, primary_key=True)
    data_publicare = db.Column(db.DateTime)
    descriere = db.Column(db.UnicodeText)
    url_document = db.Column(db.String(200))
    termen_recomandari = db.Column(db.DateTime)
    imbunatatire = db.Column(db.UnicodeText, nullable=True)
    imbunatatire_url = db.Column(db.String(200), nullable=True)


    def __init__(self, numar_proiect, data_publicare, descriere, url_document, termen_recomandari, imbunatatire=None, imbunatatire_url=None):
        self.numar_proiect = numar_proiect
        self.data_publicare = data_publicare
        self.descriere = descriere
        self.url_document = url_document
        self.termen_recomandari = termen_recomandari
        self.imbunatatire = imbunatatire
        self.imbunatatire_url = imbunatatire_url
