from flask import current_app, request

def local_request(url = None):
    """ Determines whether or not a request is local or not """
    if url is not None:
        pass
    elif request.referrer:
        url = request.referrer
    else:
        raise ValueError('Unable to determine if the request is local or not')

    # Perform basic referrer checking
    if not url.startswith(current_app.config['LOCAL_REQUEST']):
        return False

    # Return true last that way we can easily add additional checks.
    return True
