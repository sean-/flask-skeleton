import sys
reload(sys)
sys.setdefaultencoding('utf-8')

from skeleton import db

PageTags = db.Table('page_tags', db.metadata,
    db.Column('page_id', db.Integer, db.ForeignKey('public.page.id')),
    db.Column('tag_id', db.Integer, db.ForeignKey('public.tag.id')),
    schema='public'
)
