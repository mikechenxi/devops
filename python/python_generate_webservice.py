# server
from datetime import datetime
from spyne import Application, rpc, ServiceBase, String
from spyne.protocol.soap import Soap11
from spyne.server.wsgi import WsgiApplication
from wsgiref.simple_server import make_server


class Hello(ServiceBase):
    @rpc(String, _returns=String)
    def world(self, string):
        return string + str(datetime.now())


application = Application([Hello], tns='http://namespace/', in_protocol=Soap11(), out_protocol=Soap11())


if __name__ == '__main__':
    wsgi_application = WsgiApplication(application)
    server = make_server('127.0.0.1', 8080, wsgi_application)
    server.serve_forever()

    
# client
from suds.client import Client

client = Client('http://127.0.0.1:8080/?wsdl')
res = client.service.world('aa')
