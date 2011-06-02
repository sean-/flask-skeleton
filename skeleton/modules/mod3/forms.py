from flaskext.wtf import Form, Required, SubmitField, TextField, URL

class PageSubmitForm(Form):
    url = TextField('URL', validators=[Required(), URL()])
    submit = SubmitField('Submit')
