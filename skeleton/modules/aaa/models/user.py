from skeleton import db

class User(db.Model):
    __table__ = db.Table(
        'user', db.metadata,
        db.Column('id', db.Integer, primary_key=True),
        db.Column('primary_email_id', db.Integer),
        schema='email')
