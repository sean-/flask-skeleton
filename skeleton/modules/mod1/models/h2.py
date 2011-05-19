from skeleton import db

# Note the conflicting variable and table name.
class H2(db.Model):
    __table__ = db.Table(
        'h2', db.metadata,
        db.Column('id', db.Integer, primary_key=True),
        db.Column('val2', db.String),
        schema='mod1')
