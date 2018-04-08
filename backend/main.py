#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Apr  6 14:30:51 2018

@author: jur
"""

import asyncio
import datetime
import random
import websockets
import json

async def send_data(websocket, path):
    while True:
        now = datetime.datetime.utcnow().isoformat() + 'Z'
        obj = {'now': now}
        await websocket.send(json.dumps(obj))
        await asyncio.sleep(random.random() * 3)

start_server = websockets.serve(send_data, '127.0.0.1', 5678)

asyncio.get_event_loop().run_until_complete(start_server)
asyncio.get_event_loop().run_forever()