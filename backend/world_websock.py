# -*- coding: utf-8 -*-
"""
Created on Sat Mar 17 12:27:15 2018

@author: PietersmaJ

TODO: 
    1. add gradient field 
    2. turn into server 
    3. add 3djs visualization 
    4. collisions 
    5. reference frame
    6.....

"""

from settings import HOST, PORT
import socket
import json
from socket_functions import sock_send_df, sock_send_grid

import concurrent.futures


import asyncio
#import datetime
import websockets
#import json

from world import world_gen
import threading

from pymongo import MongoClient
from database import db_read_df, db_update_df, db_clear, db_update_grid, db_update_dict, db_read_dict, db_insert_metrics


def send_data(websocket, path, use_socket=True):

    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    sock.connect((HOST, PORT))

    #async for message in websocket:
    #    #await process(message)
    #    print(message)
    #t = threading.Thread(target=worker, args=[websocket])
    #print(t.start())

    #consumer_task = asyncio.ensure_future(consumer_handler(websocket, path))

    #loop = asyncio.get_event_loop()
    #blocking_tasks = [
    #    loop.run_in_executor(executor, blocks, i)
    #    for i in range(6)
    #]
    #loop.run_in_executor(executor, consumera_handler, websocket, path)    

    for df, grid, metrics in world_gen(database_name='world'):
        #sock_send_grid(sock, 'world', grid['world']['x'], grid['world']['y'], grid['world']['z'])
        # do this if you want blender connectivity
        if use_socket:
            sock_send_grid(sock, df)
            sock_send_df(sock, df)

        data = {'dataframe':df.to_dict(orient='records'), 'metrics':metrics}

        #websocket.sendMessage(df.to_json(orient='records').encode('utf8'), False)
        websocket.sendMessage(json.dumps(data).encode('utf8'), False)
        #await asyncio.sleep(random.random() * 3)






#start_server = websockets.serve(handler, '0.0.0.0', 5678)
#start_server2 = websockets.serve(consumer_handler, '0.0.0.0', 5679)


#asyncio.get_event_loop().run_until_complete(start_server)
#asyncio.get_event_loop().run_until_complete(start_server2)
#asyncio.get_event_loop().run_forever()



from autobahn.twisted.websocket import WebSocketServerProtocol, \
    WebSocketServerFactory


class MyServerProtocol(WebSocketServerProtocol):

    def onConnect(self, request):
        print("Client connecting: {0}".format(request.peer))
        client = MongoClient()
        self.db = client['world']


    def onOpen(self):
        print("WebSocket connection open.")
        t = threading.Thread(target=send_data, args=[self, ""])
        print(t.start())



    def onMessage(self, payload, isBinary):
        if isBinary:
            print("Binary message received: {0} bytes".format(len(payload)))
        else:
            print("Text message received: {0}".format(payload.decode('utf8')))
            #Text message received: {"simplebot":{"speed":"2.0","reward":"1.0","penalty":"1.0"}}
            d = json.loads(payload)
            d['simplebot'] = {k:float(v) for k,v in d['simplebot'].items()}
            d['roguebot'] = {k:float(v) for k,v in d['simplebot'].items()}
            d['wigglebot'] = {k:float(v) for k,v in d['simplebot'].items()}
            settings = {'machines' : d}
#            print(settings)
            db_update_dict(self.db, 'settings', settings)
#            print('***')
#            print(db_read_dict(self.db, 'settings'))
#            print('***')	
        # echo back message verbatim
        #self.sendMessage(payload, isBinary)

    def onClose(self, wasClean, code, reason):
        print("WebSocket connection closed: {0}".format(reason))


if __name__ == '__main__':

    import sys

    from twisted.python import log
    from twisted.internet import reactor

    log.startLogging(sys.stdout)

    factory = WebSocketServerFactory(u"ws://127.0.0.1:5678")
    factory.protocol = MyServerProtocol
    # factory.setProtocolOptions(maxConnections=2)

    # note to self: if using putChild, the child must be bytes...

    reactor.listenTCP(5678, factory)
    reactor.run()

