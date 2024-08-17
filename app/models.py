from app import db


class Visitor(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    timestamp = db.Column(db.TIMESTAMP)
    ip_address = db.Column(db.String(45))
    latitude = db.Column(db.Float)
    longitude = db.Column(db.Float)
