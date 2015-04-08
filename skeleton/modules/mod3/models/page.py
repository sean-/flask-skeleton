import sys
reload(sys)
sys.setdefaultencoding('utf-8')

from skeleton import db

from .page_tags import PageTags

class Page(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    url = db.Column(db.String)
    tags = db.relationship(
        'Tag', secondary=PageTags,
        backref=db.backref('pages', lazy='dynamic'))
    __tablename__ = 'page'
    __table_args__ = {'schema':'public'}

    def __init__(self, url = url):
        self.url = url
