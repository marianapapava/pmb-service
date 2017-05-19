from flask_sqlalchemy import SQLAlchemy

from model.shared import db

class ItemSedinta(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    sedinta_id = db.Column(db.Integer, db.ForeignKey('sedinta.id'))
    sedinta = db.relationship('Sedinta', back_populates='itemuri')
    descriere = db.Column(db.UnicodeText())
    url = db.Column(db.String(200))

    def __init__(self, sedinta, descriere, url):
        self.sedinta = sedinta
        self.descriere = descriere
        self.url = url
