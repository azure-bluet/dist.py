from xmlrpc.client import Binary, ServerProxy

class ServerConf:
    def __init__ (self, addr: str, pswd: str):
        self.src = ServerProxy (addr)
        self.pswd = pswd
    def download (self, name: str, path: str) -> None:
        f = open (path, 'wb')
        f.write (self.src.read (self.pswd, [name]) [name] .data)
        f.close ()
    def upload (self, name: str, path: str) -> None:
        f = open (path, 'rb')
        data = f.read ()
        f.close ()
        self.src.write (self.pswd, {name: Binary (data)})

if __name__ == '__main__':

    from sys import argv
    if len (argv) < 3:
        addr = input ("Input server address for testing: ")
        pswd = input ("Input server password for testing: ")
    else:
        addr = argv [1]
        pswd = argv [2]
    server = ServerConf (addr, pswd)

    from os import urandom
    f = open ('1.test', 'wb')
    f.write (urandom (15))
    f.close ()
    server.upload ('u.w.u', '1.test')

    server.download ('u.w.u', '2.test')
    f1 = open ('1.test', 'rb') .read ()
    f2 = open ('2.test', 'rb') .read ()
    if f1 == f2 and f1: print ('Success!')
    else: print ('Fail!')
