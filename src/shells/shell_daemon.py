from flask import Flask, request
import json

from src.shells.daemon_manager import Order

class ShellDaemon:
    def __init__(self, parent, host, port):
        self.parent = parent

        self.host = host
        self.port = port

    def run(self, i):
        app = Flask("Daemon #{}".format(i))

        def parse_order(encoded_order: str) -> Order:
            decoded_order = json.dumps(encoded_order)
            return Order(decoded_order["command"], decoded_order["args"])

        @app.route("/", methods=['POST'])
        def handle_order():
            self.parent.execute(parse_order(request.get_json()))

        app.run(self.host, self.port)
