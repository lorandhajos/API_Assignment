from gevent.pywsgi import WSGIServer

from app import app

IP = "127.0.0.1"
PORT = 8000

print("Starting server", IP, "on port", PORT)

http_server = WSGIServer((IP, PORT), app)
http_server.serve_forever()
