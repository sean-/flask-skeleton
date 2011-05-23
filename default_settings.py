# Global configuration
BROWSER_SECRET_KEY = ''
DATABASE_URI_FMT = 'postgresql+psycopg2://{username}:{password}@{hostname}:{port}/{dbname}'
DB_HOST = '127.0.0.1'
DB_NAME = 'skeleton'
# Setup a password database. Generate a random pass via:
# import OpenSSL
# OpenSSL.rand.bytes(24).encode('base64')[:32]
DB_PASS = ''
DB_PORT = '5432'
DB_SCHEMA = 'skeleton_schema'
DB_ADMIN = 'skeleton_admin'
DB_USER = 'skeleton_www'
DEBUG = False
DEBUG_TOOLBAR = False
PASSWORD_HASH = ''
SECRET_KEY = ''
SESSION_COOKIE_NAME = 'skeleton_session'
TESTING = False

# Logs SQL queries to stderr
SQLALCHEMY_ECHO = False

# Import user-provided values
try:
    from local_settings import *
except ImportError:
    pass

# Add a small amount of anti-footshooting and check to make sure a browser
# key is set.
if len(BROWSER_SECRET_KEY) < 16:
    # Generate a a good key
    import OpenSSL, os, re
    randpw = re.sub(os.linesep, '', OpenSSL.rand.bytes(24).encode('base64')[:32])
    print "Generating a random password for BROWSER_SECRET_KEY. Copy/paste the following commands to setup a random non-fail password."
    print '\n\techo "BROWSER_SECRET_KEY = \'%s\'" >> local_settings.py\n' % randpw
    raise ValueError('BROWSER_SECRET_KEY needs to be set and longer than 8 characters (len(BROWSER_SECRET_KEY) >= 16 recommended)!')

# Add a small amount of anti-footshooting and check to make sure a password
# is set. Idiots use passwords less than 16char. Just sayin'.
if len(DB_PASS) < 8:
    # Generate a 29char random password. Good enough.
    import OpenSSL, os, re
    randpw = re.sub(os.linesep, '', OpenSSL.rand.bytes(24).encode('base64')[:32])
    print "Generating a random password for DB_PASS. Copy/paste the following commands to setup a random non-fail password."
    print '\n\techo "DB_PASS = \'%s\'" >> local_settings.py\n' % randpw
    raise ValueError('DB_PASS needs to be set and longer than 8 characters (len(DB_PASS) >= 16 recommended)!')

# Add a small amount of anti-footshooting and check to make sure a password
# hash is set of modest strength.
if len(PASSWORD_HASH) < 32:
    # Generate a decently long random secret.
    import OpenSSL
    randsec = re.sub(os.linesep, '', OpenSSL.rand.bytes(256).encode('base64'))
    print "Generating a random secret for PASSWORD_HASH. Copy/paste the following commands to setup a random non-fail secret.\n"
    print '\techo "PASSWORD_HASH = \'%s\'.decode(\'base64\')" >> local_settings.py\n' % randsec
    print "DO NOT LOOSE PASSWORD_HASH! If you loose PASSWORD_HASH no users will be able to log in and every user will have to reset their password!!!\n"
    raise ValueError('PASSWORD_HASH needs to be set and longer than 32 characters (len(PASSWORD_HASH) >= 32 recommended)!')

# Add a small amount of anti-footshooting and check to make sure a secret key
# is set of modest strength.
if len(SECRET_KEY) < 32:
    # Generate a decently long random secret.
    import OpenSSL
    randsec = re.sub(os.linesep, '', OpenSSL.rand.bytes(256).encode('base64'))
    print "Generating a random secret for SECRET_KEY. Copy/paste the following commands to setup a random non-fail secret.\n"
    print '\techo "SECRET_KEY = \'%s\'.decode(\'base64\')" >> local_settings.py\n' % randsec
    raise ValueError('SECRET_KEY needs to be set and longer than 32 characters (len(SECRET_KEY) >= 64 recommended)!')

# Derived values
SQLALCHEMY_DATABASE_URI = DATABASE_URI_FMT.format(**
    {   'username': DB_USER,
        'password': DB_PASS,
        'hostname': DB_HOST,
        'port':     DB_PORT,
        'dbname':   DB_NAME,
        'schema':   DB_SCHEMA,
    })
