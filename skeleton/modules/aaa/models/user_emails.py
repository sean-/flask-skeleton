import sys
reload(sys)
sys.setdefaultencoding('utf-8')

from skeleton import db


class UserEmails(db.Model):
    __table__ = db.Table(
        'user_emails', db.metadata,
        db.Column('user_id', db.Integer, primary_key=True),
        db.Column('email_id', db.Integer),
        db.Column('email', db.String),
        db.Column('user_primary_email_id', db.Integer),
        schema='email')
