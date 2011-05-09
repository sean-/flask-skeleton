from skeleton import app
from skeleton.database import create_db

if __name__ == '__main__':
    create_db(schema_name=app.config['DB_SCHEMA'],
              admin_name=app.config['DB_ADMIN'],
              user_name=app.config['DB_USER'])

