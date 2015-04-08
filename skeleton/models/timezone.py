import sys
reload(sys)
sys.setdefalutencoding = 'utf-8'

from skeleton import db

class Timezone(db.Model):
    __table__ = db.Table(
        'timezone', db.metadata,
        db.Column('id', db.Integer, primary_key=True),
        db.Column('name', db.String),
        schema='public')
