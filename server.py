import os, ssl
from random import choice
from socketserver import TCPServer
from xmlrpc.client import Binary
from xmlrpc.server import SimpleXMLRPCDispatcher, SimpleXMLRPCRequestHandler

class SSLServer (TCPServer):

    context = ssl.SSLContext (ssl.PROTOCOL_TLS_SERVER)
    context.load_cert_chain ("certs/ssl.pem", "certs/ssl.key")

    def get_request(self):
        newsocket, fromaddr = self.socket.accept ()
        connstream = self.context.wrap_socket (newsocket, server_side=True)
        return (connstream, fromaddr)

class SSLXMLRPCServer (SSLServer, SimpleXMLRPCDispatcher):

    allow_reuse_address = True

    def __init__ (self, addr, requestHandler=SimpleXMLRPCRequestHandler,
                  logRequests=True, allow_none=True, encoding=None, bind_and_activate=True):
        
        self.logRequests = logRequests
        SimpleXMLRPCDispatcher.__init__ (self, allow_none, encoding)
        SSLServer.__init__ (self, addr, requestHandler, bind_and_activate)
D = [chr (i) for i in range (48, 58)] + [chr (i) for i in range (97, 123)] + list ('+-*/')
DF = lambda: ''.join ([choice (D) for i in range (74)])

if not os.path.exists ('file'): os.mkdir ('file')
password = open ("password.txt") .read ()

def verify (pswd: str) -> bool:
    return pswd == password

def read (pswd: str, names: list [str]) -> dict [str, Binary] | None:
    if pswd != password: return
    ret = {}
    for name in names:
        if '/' not in name:
            f = open ('./file/' + name, 'rb')
            ret [name] = Binary (f.read ())
            f.close ()
    return ret

def write (pswd: str, names = dict [str, Binary]) -> None:
    if pswd != password: return
    for name in names:
        if '/' not in name:
            f = open ('./file/' + name, 'wb')
            f.write (names [name] .data)
            f.close ()

server = SSLXMLRPCServer (("", 2952))
server.register_function (verify)
server.register_function (read)
server.register_function (write)
server.serve_forever ()
