import os
import tornado.ioloop
import tornado.web
import tornado.httpserver
from handlers.pages import IndexHandler 
from handlers.query import QueryHandler


class Application(tornado.web.Application):

    PORT = 8888

    def __init__(self):

        handlers = [
            tornado.web.URLSpec(r'/', IndexHandler),
            tornado.web.URLSpec(r'/search', QueryHandler)

            # API
        ]
        current_dir = os.path.dirname(__file__)

        settings = dict(
            template_path=os.path.join(current_dir, 'templates'),
            static_path=os.path.join(current_dir, 'static'),
            cookie_secret='947e5d1dc624bc99421bfc7e8ebad245'
        )

        super(Application, self).__init__(handlers, **settings)

    def start(self):
        """Start the application."""
        server = tornado.httpserver.HTTPServer(Application())
        server.listen(Application.PORT)
        tornado.ioloop.IOLoop.instance().start()

if __name__ == "__main__":
    """Start application upon running this file."""
    app = Application()
    app.start()

