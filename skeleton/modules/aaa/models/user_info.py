from skeleton import db

class UserInfo(db.Model):
    timezone_id = db.Column(db.Integer, db.ForeignKey('public.timezone.id'))
    timezone = db.relationship('Timezone', primaryjoin='Timezone.id==UserInfo.timezone_id')

    user_id = db.Column(db.Integer, primary_key=True)

    __tablename__ = 'user_info'
    __table_args__ = {'schema':'aaa'}
