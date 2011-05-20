from skeleton import db

class H1(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    val = db.Column(db.String)
    __table_args__ = {'schema':'public'}
