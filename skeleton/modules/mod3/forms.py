import re

from flaskext.wtf import Form, Regexp, Required, SubmitField, TextField, URL

class PageAddTagForm(Form):
    tag = TextField('Tag', validators=[
            Required(),
            Regexp(regex=r'[a-z0-9]{1,80}', flags=re.IGNORECASE, message='Invalid Tag. Only able to use a-z and 0-9'),
            ])
    submit = SubmitField('Submit')


class PageSubmitForm(Form):
    url = TextField('URL', validators=[Required(), URL()])
    submit = SubmitField('Submit')
