from flask_sqlalchemy import SQLAlchemy

from model.shared import db

class Sedinta(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    data = db.Column(db.DateTime)
    itemuri = db.relationship('ItemSedinta', back_populates='sedinta', cascade='save-update, merge, delete')

    def __init__(self, data):
        self.data = data
