from server import HTTPServer, HTTPTemplate
from config import *

server = HTTPServer(host=Config.host.value, port=Config.port.value, static="./static")


@server.route("/", methods=["GET"])
def index():
    return HTTPTemplate.html("<h1>Hello h1</h1><h2>Hello h2</h2>")


# В браузере GET вызовет 405
@server.route("/test.html", methods=["POST"])
def index():
    return HTTPTemplate.html("<h1>Hello h1</h1><h2>Hello h2</h2>")


@server.route("/test.json", methods=["GET"])
def test_json():
    with open("./static/j.json", "r") as j:
        return HTTPTemplate.other_type("".join(j.readlines()), type="JSON")


@server.route("/logs.log", methods=["GET"])
def logs():
    try:
        with open("server.log", "r") as f:
            return HTTPTemplate.other_type("".join(f.readlines()), type="None")
    except FileNotFoundError:
        return HTTPTemplate.html("")


server.run()
