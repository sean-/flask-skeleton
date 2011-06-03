# Global configuration
BROWSER_SECRET_KEY = ''

# Flask-Cache settings
CACHE_TYPE = 'memcached'
CACHE_MEMCACHED_SERVERS = ['127.0.0.1:11211']

# When behind a load balancer, set CANONICAL_NAME to the value contained in
# Host headers (e.g. 'www.example.org')
CANONICAL_NAME = '127.0.0.1'

# When behind a load balancer, set CANONICAL_PORT to the value contained in
# Host headers (normally it will be '80' in production)
CANONICAL_PORT = '5000'

DATABASE_URI_FMT = 'postgresql+psycopg2://{username}:{password}@{hostname}:{port}/{dbname}'
DB_HOST = '127.0.0.1'
DB_NAME = 'skeleton'
# Setup a password database. Generate a random pass via:
# import M2Crypto
# M2Crypto.m2.rand_bytes(24).encode('base64').rstrip()
DB_PASS = ''
DB_PORT = '5432'
DB_SCHEMA = 'skeleton_schema'
DB_ADMIN = 'skeleton_admin'
DB_USER = 'skeleton_www'
DEBUG = False
DEBUG_TOOLBAR = False
LISTEN_HOST = '127.0.0.1'
PASSWORD_HASH = ''
SECRET_KEY = ''
SESSION_BYTES = 25
SESSION_COOKIE_NAME = 'skeleton_session'
SSL_CERT_FILENAME = ''
SSL_PRIVATE_KEY_FILENAME = ''
TESTING = False
USE_SSL = True

# Logs SQL queries to stderr
SQLALCHEMY_ECHO = False

# If users want to pass specific werkzeug options
WERKZEUG_OPTS = {'host': LISTEN_HOST, 'port' : 5000}

# Import user-provided values
try:
    from local_settings import *
except ImportError:
    pass


# Add a small amount of anti-footshooting and check to make sure a browser
# key is set.
if len(BROWSER_SECRET_KEY) < 16:
    # Generate a a good key
    import M2Crypto, os, re
    randpw = re.sub(os.linesep, '', M2Crypto.m2.rand_bytes(24).encode('base64').rstrip())
    print "Generating a random password for BROWSER_SECRET_KEY. Copy/paste the following commands to setup a random non-fail password."
    print '\n\techo "BROWSER_SECRET_KEY = \'%s\'" >> local_settings.py\n' % randpw
    raise ValueError('BROWSER_SECRET_KEY needs to be set and longer than 8 characters (len(BROWSER_SECRET_KEY) >= 16 recommended)!')


# Add a small amount of anti-footshooting and check to make sure a password
# is set. Idiots use passwords less than 16char. Just sayin'.
if len(DB_PASS) < 8:
    # Generate a 29char random password. Good enough.
    import M2Crypto, os, re
    randpw = re.sub(os.linesep, '', M2Crypto.m2.rand_bytes(24).encode('base64').rstrip())
    print "Generating a random password for DB_PASS. Copy/paste the following commands to setup a random non-fail password."
    print '\n\techo "DB_PASS = \'%s\'" >> local_settings.py\n' % randpw
    raise ValueError('DB_PASS needs to be set and longer than 8 characters (len(DB_PASS) >= 16 recommended)!')


# Add a small amount of anti-footshooting and check to make sure a password
# hash is set of modest strength.
if len(PASSWORD_HASH) < 32:
    # Generate a decently long random secret.
    import M2Crypto, os, re
    randsec = re.sub(os.linesep, '', M2Crypto.m2.rand_bytes(256).encode('base64').rstrip())
    print "Generating a random secret for PASSWORD_HASH. Copy/paste the following commands to setup a random non-fail secret.\n"
    print '\techo "PASSWORD_HASH = \'%s\'.decode(\'base64\')" >> local_settings.py\n' % randsec
    print "DO NOT LOOSE PASSWORD_HASH! If you loose PASSWORD_HASH no users will be able to log in and every user will have to reset their password!!!\n"
    raise ValueError('PASSWORD_HASH needs to be set and longer than 32 characters (len(PASSWORD_HASH) >= 32 recommended)!')


# Add a small amount of anti-footshooting and check to make sure a secret key
# is set of modest strength.
if len(SECRET_KEY) < 32:
    # Generate a decently long random secret.
    import M2Crypto, os, re
    randsec = re.sub(os.linesep, '', M2Crypto.m2.rand_bytes(256).encode('base64').rstrip())
    print "Generating a random secret for SECRET_KEY. Copy/paste the following commands to setup a random non-fail secret.\n"
    print '\techo "SECRET_KEY = \'%s\'.decode(\'base64\')" >> local_settings.py\n' % randsec
    raise ValueError('SECRET_KEY needs to be set and longer than 32 characters (len(SECRET_KEY) >= 64 recommended)!')


# If we're running in SSL mode, check for the files or give users a hint on
# how to generate the keys.
if USE_SSL:
    import os
    key_file = SSL_PRIVATE_KEY_FILENAME if SSL_PRIVATE_KEY_FILENAME else 'ssl.key'
    cert_file = SSL_CERT_FILENAME if SSL_CERT_FILENAME else 'ssl.cert'
    if not os.access(key_file, os.R_OK) and not os.access(cert_file, os.R_OK):
        print "HINT: To generate a key and cert without it prompting for information (spaces are escaped with a \\):\n"
        print "\topenssl req -x509 -nodes -days 365 -subj '/C=US/ST=MyState/L=MyCity/CN=127.0.0.1/O=MyCompany\ Inc/OU=MyOU/emailAddress=user@example.com' -newkey rsa:1024 -keyout %s -out %s\n" % (key_file, cert_file)
        raise ValueError('SSL_PRIVATE_KEY_FILENAME file missing (possibly needs to be generated?)')

    else:
        if not os.access(key_file, os.R_OK):
            print "HINT: To generate a private key:\n"
            print "\topenssl genrsa 1024 > %s\n" % key_file
            raise ValueError('SSL_PRIVATE_KEY_FILENAME file missing (possibly needs to be generated?)')

        if not os.access(cert_file, os.R_OK):
            print "HINT: To generate a private key:\n"
            print "\topenssl req -new -x509 -nodes -sha1 -days 365 -key %s > %s\n" % (key_file, cert_file)
            raise ValueError('SSL_CERT_FILENAME file missing (possibly needs to be generated?)')

    from OpenSSL import SSL
    ctx = SSL.Context(SSL.TLSv1_METHOD)
    ctx.use_privatekey_file(key_file)
    ctx.use_certificate_file(cert_file)
    WERKZEUG_OPTS['ssl_context'] = ctx

    ### WARNING: Ugh. Monkey pach in a fix to correct pyOpenSSL's
    ### incompatible ServerSocket implementation that accepts zero arguments
    ### for shutdown() instead of one. Fix up
    ### lib/python2.7/SocketServer.py:459's shutdown() call because that
    ### appears to be easier to quickly hack in versus patching
    ### pyOpenSSL. Again, don't use this for production, but it's great for
    ### testing.
    def monkeyp_ssl_shutdown_request(self, request):
        try:
            request.shutdown()
        except socket.error:
            pass #some platforms may raise ENOTCONN here
        self.close_request(request)
    from SocketServer import TCPServer
    TCPServer.shutdown_request = monkeyp_ssl_shutdown_request



# Derived values
SQLALCHEMY_DATABASE_URI = DATABASE_URI_FMT.format(**
    {   'username': DB_USER,
        'password': DB_PASS,
        'hostname': DB_HOST,
        'port':     DB_PORT,
        'dbname':   DB_NAME,
        'schema':   DB_SCHEMA,
    })

# Explicitly specify what's a local request
scheme = 'https' if USE_SSL else 'http'
LOCAL_REQUEST = '%s://%s:%s/' % (scheme, CANONICAL_NAME, CANONICAL_PORT)
