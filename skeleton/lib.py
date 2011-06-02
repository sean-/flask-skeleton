from flask import current_app, request, session

from aaa import LOGIN_SUFFIX_BLACKLIST

def fixup_destination_url(src_param_name, dst_param_name):
    """ Saves the destination URL tagged as a URL parameter or in the session and
    moves it over to a local session variable. Useful when you want to
    capture the last value of something, but a user could possibly walk
    off. """
    local_dsturl = None
    if src_param_name in session:
        # SecureCookie sessions are tamper proof, supposedly. Don't need to
        # check if its a trusted parameter.
        local_dsturl = session.pop(src_param_name)
    elif src_param_name in request.args and local_request(request.args[src_param_name]):
        # Request parameters are spoofable, always check and only accept
        # trusted arguments.
        local_dsturl = request.args[src_param_name]

    # Return if nothing was found in the arguments
    if not local_dsturl:
        return False
    else:
        # If something was found, remove our destination
        session.pop(dst_param_name, None)

    for suffix in LOGIN_SUFFIX_BLACKLIST:
        # XXX: This should be a bit more sophisticated and use a
        # regex that ignores query parameters.
        if local_dsturl.endswith(suffix) and LOGIN_SUFFIX_BLACKLIST[suffix]:
            local_dsturl = None
            break

    if local_dsturl:
        session[dst_param_name] = local_dsturl
    return True


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
