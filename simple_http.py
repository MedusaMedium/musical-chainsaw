#!/usr/bin/env python3
'''
how do i get the colors working on windows terminal?
'''
import argparse
import http.server
import os
import socket
import socketserver
import sys

CYN_ISH = ""
UND     = ""
RESET   = ""
if sys.platform.startswith("linux"):
    CYN_ISH = "\033[92m"
    UND     = "\033[04m"
    RESET   = "\033[00m"

Handler = http.server.SimpleHTTPRequestHandler

def cmdln():
    parser = argparse.ArgumentParser()
    parser.add_argument("-d","--directory",
        type=lambda d:os.path.abspath(d) if os.path.isdir(d) else parser.error("invalid directory"),
        default=os.getcwd(),help="directory to expose")
    parser.add_argument("-p","--port",type=int,required=False,default=8000,
        help="port to serve on. default 8000")
    parser.add_argument("--local",action="store_true",required=False,default=False)
    return parser.parse_args()

if __name__ == "__main__":
    args = cmdln()
    if args.directory != os.getcwd():
        os.chdir(path)
    addr = ext_addr = ""
    if args.local:
        addr = "127.0.0.1"
    else:
        s = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
        ext_addr = socket.gethostbyname(socket.gethostname())
        s.close()
    with socketserver.TCPServer((addr, args.port), Handler) as httpd:
        print(
            f"Serving {CYN_ISH}{args.directory}{RESET} on "+
            f"{UND}{[ext_addr, httpd.server_address[0]][args.local]}:"+
            f"{httpd.server_address[1]}{RESET}..."
        )
        httpd.serve_forever()