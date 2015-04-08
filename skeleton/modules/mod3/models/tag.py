import sys
reload(sys)
sys.setdefaultencoding('utf-8')

from skeleton import db


class Tag(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String)

    # Placeholders:
    # pages is created automatically via the Page model
    __tablename__ = 'tag'
    __table_args__ = {'schema':'public'}
