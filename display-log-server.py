#!/usr/bin/env python3

import socketserver
import urllib.parse
import requests
import os
import re

BIND_HOST="0.0.0.0"
BIND_PORT=9999

MMM_HOST="localhost"
MMM_PORT=8080

SCREEN_TIMOUT=120

def activate_screen():
    os.system(f"export DISPLAY=:0; xset s {SCREEN_TIMOUT}; xset s reset; xset s default")
    
class MyTCPHandler(socketserver.StreamRequestHandler):
    
    def handle(self):
        line = self.rfile.readline().strip().decode("utf-8").split()
        if line:
            if len(line) == 1 and line[0] == "help":
                self.wfile.write(b"OK Usage: [INFO|WARNING|ERROR] <from-hostname> <message>\n")
                
            elif len(line) >= 2:
                message_type = line[0].upper()
                message = ' '.join(line[1:])
                
                if message_type not in ['INFO', 'WARNING', 'ERROR']:
                    self.wfile.write(b"NOK Invalid message type.\n")
                    return

                # Remove everything that is not on a white list.
                message = re.sub("[^A-Za-z0-9\.\:\!\?\,\-\_\(\)\\[\\]]", ' ', message)
                
                url = "http://%s:%s/syslog?type=%s&message=%s&silent=true" % \
                      (MMM_HOST, MMM_PORT, message_type,
                       urllib.parse.quote(message))
                
                r = requests.get(url=url)
                if not r:
                     self.wfile.write(b"NOK HTTP GET error")                    
                elif r.status_code == 200:     
                    activate_screen()
                    self.wfile.write(b"OK\n")
                else:
                    self.wfile.write(b"NOK Status code" + str(r.status_code) + "\n")
                    
            else:
                self.wfile.write(b"NOK Unknown Command\n")
        else:
            self.wfile.write(b"NOK Can't parse line\n")

if __name__ == "__main__":
    socketserver.TCPServer.allow_reuse_address = True
    server = socketserver.TCPServer((BIND_HOST, BIND_PORT), MyTCPHandler)
    server.serve_forever()
