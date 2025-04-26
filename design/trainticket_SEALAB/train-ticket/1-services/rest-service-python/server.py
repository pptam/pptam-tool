import tornado.ioloop
import tornado.web

class MainHandler(tornado.web.RequestHandler):
    def get(self):
        self.write("Hello, world")

class TestHandler(tornado.web.RequestHandler):
    def get(self):
        self.write("testing")

class Test1Handler(tornado.web.RequestHandler):
    def get(self):
        self.write("testing ------ 2")

def make_app():
    return tornado.web.Application([
        (r"/", MainHandler),
        (r"/test", TestHandler),
        (r"/test1", Test1Handler),
    ])

if __name__ == "__main__":
    app = make_app()
    app.listen(16101)
    tornado.ioloop.IOLoop.current().start()


    