from skeleton import create_app

app = create_app(__name__)

if app.config['DEBUG']:
    app.debug = True

app.run()
