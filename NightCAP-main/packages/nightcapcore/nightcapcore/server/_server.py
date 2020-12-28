# Copyright 2020 by Aaron Baker.
# All rights reserved.
# This file is part of the Nightcap Project,
# and is released under the "MIT License Agreement". Please see the LICENSE
# file that should have been included as part of this package.
import argparse
import os
import socketserver
from http.server import BaseHTTPRequestHandler
from nightcapcore.server.reporting_server_base import NightcapCoreServerReportingBase

class SimpleHttpRequestHandler(BaseHTTPRequestHandler):
    def do_HEAD(self):
        return

    def do_POST(self):
        return

    def do_GET(self):
        self.respond()
 
    def respond(self):
        if(".css" in self.path):
            content = self.handle_http(200, 'text/css')
        else:
            content = self.handle_http(200, 'text/html')
        self.wfile.write(content)
 
    def handle_http(self, status, content_type):
        print("requested: ", self.path)
        self.send_response(status)
        self.send_header("Content-type", content_type)
        self.end_headers()
        print("Current Path:", os.path.dirname(__file__))

        route_content = NightcapCoreServerReportingBase(os.path.join(os.path.dirname(__file__), "webbase")).get_route(self.path)
        return bytes(route_content, 'UTF-8')

if __name__ == '__main__':
    try:
        parser = argparse.ArgumentParser(description='Process some server inputs.')
        parser.add_argument('--ip', required=True, dest="ip",
                            help='lip')
        parser.add_argument('--port', required=True, dest="port",
                            help='port')
        args = parser.parse_args()
        
        httpd = socketserver.TCPServer((args.ip, int(args.port)), SimpleHttpRequestHandler)
        httpd.serve_forever()
    except Exception as e:
        print(e)
