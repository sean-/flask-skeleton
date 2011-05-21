from skeleton import db

class Email(db.Model):
    __table__ = db.Table(
        'email', db.metadata,
        db.Column('id', db.Integer, primary_key=True),
        db.Column('email', db.String),
        db.Column('user_id', db.Integer),
        schema='aaa')
