from pprint import pformat
from urllib.parse import parse_qsl

HELLO_WORLD = b'Hello, world!\n'
FORM = b"""<p>WSGI DATA<p>
<p>POST data collect form<p>
<form method="post">
<input type="text" name="test">
<input type="submit" value="send">
</form>"""


def simple_app(environ, start_response):
    status = '200 OK'
    print(environ)
    response_headers = [('Content-Type', 'text/plain')]
    start_response(status, response_headers)
    return [HELLO_WORLD]


def get_post_params(environ, start_response):
    if environ['REQUEST_METHOD'] == 'POST':
        print('POST data')
        print(pformat(environ['wsgi.input'].read()))
    if environ['REQUEST_METHOD'] == 'GET':
        print('GET data')
        print(parse_qsl(environ['QUERY_STRING']))
    response_headers = [('Content-type', 'text/html'),
                        ('Content-Length', str(len(FORM)))]
    start_response('200 OK', response_headers)
    return [FORM]


# application = get_post_params


class GetSetParamsClass:
    def __init__(self, environ, start_response):
        self.environ = environ
        self.start = start_response

    def __iter__(self):
        status = '200 OK'
        if self.environ['REQUEST_METHOD'] == 'POST':
            print('POST data')
            print(pformat(self.environ['wsgi.input'].read()))
        if self.environ['REQUEST_METHOD'] == 'GET':
            print('GET data')
            print(parse_qsl(self.environ['QUERY_STRING']))
        response_headers = [('Content-type', 'text/html'),
                            ('Content-Length', str(len(FORM)))]
        self.start(status, response_headers)
        yield FORM


application = GetSetParamsClass
