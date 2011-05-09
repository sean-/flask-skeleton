from skeleton import app

if app.config['DEBUG']:
    app.debug = True

if __name__ == '__main__':
    app.run()
