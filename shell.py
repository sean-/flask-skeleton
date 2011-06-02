from skeleton import create_app
app = create_app()
ctx = app.test_request_context()
ctx.push()
from skeleton import db
ses = db.session
