'''
@author: Jason Rodd
minimal thread to connect to gdax websocket for real time data
dispatcher is a Priority Queue. As we receive messages from the websocket we Enqueue them.
Dequeueing messages maintain the order we received them.
Allows for our logic to be in a different thread then the datafeed.
'''

import json, hmac, hashlib, time, requests, base64
from websocket import *
import threading
import queue


class DataFeed(threading.Thread):
    def __init__(self, threadID, message_type="subscribe", api_key=None, secret_key=None, passphrase=None, products=["BTC-USD"], channels=[]):
        threading.Thread.__init__(self)
        self.url = "wss://ws-feed.gdax.com"
        self.isRunning = False
        self.threadID = threadID
        
        if api_key is not None:
            self.api_key = api_key
            self.secret_key = secret_key
            self.passphrase = passphrase
            self.auth = True
        else:
            self.auth = False
        
        if not isinstance(products, list) or not isinstance(channels, list):
            return "Bad product or channel"   

        self.products = products
        self.channels = channels
        self.heartBeart = False
        self.ws = None
        
        self.dispatcher = queue.PriorityQueue()
    
    def run(self):
        self.isRunning = True
        self.connect()
        while self.isRunning:
            self.Enqueue(self.listen())
        
    def connect(self):
        parameters = {"type":"subscribe","product_ids":self.products,"channels":self.channels}
        
        if self.auth:
            timestamp = str(time.time())
            message = timestamp + 'GET' + '/users/self/verify'
            message = message.encode('ascii')
            hmac_key = base64.b64decode(self.secret_key)
            signature = hmac.new(hmac_key, message, hashlib.sha256)
            signature_b64 = base64.b64encode(signature.digest()).decode('utf-8')
            parameters['signature'] = signature_b64
            parameters['key'] = self.api_key
            parameters['passphrase'] = self.passphrase
            parameters['timestamp'] = timestamp
        
        self.ws = create_connection(self.url)
        self.ws.send(json.dumps(parameters))

    def listen(self):
        try:
            data = self.ws.recv()
            return data
        except Exception as e:
            pass
        
    
    def Unsubscribe(self,channels=[]):
            if not isinstance(channels, list):
                return "bad Channels"
            else:
                message = {"type":"unsubscribe","channels":channels}
                self.ws.send(json.dumps(message))
       
    
    def disconnect(self):
        self.isRunning = False
        try:
            self.ws.close()
        except WebSocketConnectionClosedException as e:
            pass
    
    
    def Enqueue(self,message=None):
        if message is not None:
            self.dispatcher.put(message)
    
    def Dequeue(self):
        if not self.isEmpty():
            return self.dispatcher.get()  
        
    def isEmpty(self):
        return self.dispatcher.empty()
        