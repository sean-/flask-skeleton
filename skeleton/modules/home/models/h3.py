from skeleton import db

class H3(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    val2 = db.Column(db.String)
    __table_args__ = {'schema':'public'}
