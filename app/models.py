from . import db
from datetime import datetime

class Review(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    pokemon_name = db.Column(db.String(50), nullable=False)
    rating = db.Column(db.Integer)
    comment = db.Column(db.Text)
    user_ip = db.Column(db.String(50))
    user_agent = db.Column(db.String(200))
    created_at = db.Column(db.TIMESTAMP, server_default=db.func.current_timestamp(), nullable=False)
