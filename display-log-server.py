#!/usr/bin/env python3

import socketserver
import urllib.parse
import requests
import os

BIND_HOST="0.0.0.0"
BIND_PORT=9999

MMM_HOST="localhost"
MMM_PORT=8080

def activate_screen():
    os.system("xset s reset")
    
class MyTCPHandler(socketserver.StreamRequestHandler):
    
    def handle(self):
        line = self.rfile.readline().strip().decode("utf-8").split()
        if line:
            if len(line) == 1 and line[0] == "help":
                self.wfile.write(b"OK Usage: <from-hostname> [INFO|WARNING|ERROR] <message>\n")
                
            elif len(line) >= 3:
                host = line[0]
                message_type = line[1].upper # info, warning, error
                message = ' '.join(line[2:])

                if message_type not in ['INFO', 'WARNING', 'ERROR']:
                    self.wfile.write(b"NOK Invalid message type.\n")
                    return
                
                url = "http://%s:%s/syslog?type=%s&message=%s&silent=true" % \
                      (MMM_HOST, MMM_PORT, message_type,
                       urllib.parse.quote(message))
                
                r = requests.get(url=url)
                if r.status_code == 200:                                 
                    self.wfile.write(b"OK\n")
                    activate_screen()
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
