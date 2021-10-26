import requests as _requests


def getPageText(url):
    # initialize session
    sess = _requests.session()

    # request the URL
    response = sess.get(url)

    # Return text
    return response.text


def unescape(s):
    s = s.replace("&lt;", "<")
    s = s.replace("&gt;", ">")
    # this has to be last:
    s = s.replace("&amp;", "&")
    return s
