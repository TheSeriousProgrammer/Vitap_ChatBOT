import tornado.httpserver
import tornado.ioloop
import tornado.web

class getToken(tornado.web.RequestHandler):
    def get(self):
        self.write("hello")

application = tornado.web.Application([
    (r'/', getToken),
])

if __name__ == '__main__':
    http_server = tornado.httpserver.HTTPServer(application, ssl_options={
        "certfile": "/etc/letsencrypt/live/vitapchatbot.duckdns.org/fullchain_copy.pem",
        "keyfile": "/etc/letsencrypt/live/vitapchatbot.duckdns.org/privkey_copy.pem"
    })
    http_server.listen(4431)
    tornado.ioloop.IOLoop.instance().start()
