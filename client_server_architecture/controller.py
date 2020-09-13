from tornado.web import RequestHandler


class Controller(RequestHandler):
    ml_module = None
