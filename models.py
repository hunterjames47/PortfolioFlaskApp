from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
db = SQLAlchemy()

class Note(db.Model):
    __tablename__="note"
    id = db.Column(db.Integer, primary_key=True)
    nickname= db.Column(db.String(50), nullable=False)
    content = db.Column(db.String(200), nullable=False)
    active=db.Column(db.Boolean, default=True, nullable=False)
    date_created = db.Column (db.DateTime, default =datetime.utcnow)
    date_updated= db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    history = db.relationship("NoteHistory", backref="note", passive_deletes=True)

class NoteHistory(db.Model):
    __tablename__ = "note_history"
    __table_args__ = {"schema": "history"}

    id=db.Column(db.Integer, primary_key=True)
    note_id=db.Column(db.Integer, db.ForeignKey("note.id"), nullable=False)
    version=db.Column(db.Integer, nullable=False)
    nickname=db.Column(db.String(50), nullable=False)
    content=db.Column(db.Text, nullable=False)
    timestamp=db.Column(db.DateTime, default=datetime.utcnow)