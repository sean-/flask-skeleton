import sys
reload(sys)
sys.setdefaultencoding('utf-8')

from skeleton import db

class User(db.Model):
    active = db.Column(db.Boolean)
    default_ipv4_mask = db.Column(db.Integer)
    default_ipv6_mask = db.Column(db.Integer)
    max_concurrent_sessions = db.Column(db.Integer)
    registration_utc = db.Column(db.DateTime(timezone=True))
    timezone_id = db.Column(db.Integer, db.ForeignKey('public.timezone.id'))
    timezone = db.relationship('Timezone', primaryjoin='Timezone.id==User.timezone_id')
    user_id = db.Column(db.Integer, primary_key=True)

    __tablename__ = 'user'
    __table_args__ = {'schema':'aaa'}
