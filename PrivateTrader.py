'''
@author: Jason Rodd
Used to connect directly to your account to buy and sell on gdax
Does not include any functionality for withdrawal/deposit transferring, stop orders or margin trading because I don't care for that stuff. 
'''

import json, hmac, hashlib, time, requests, base64
from requests.auth import AuthBase

class Trader():
    
    def __init__(self, api_key, secret_key, passphrase):
        self.url = 'https://api.gdax.com'
        self.api_key = api_key
        self.secret_key = secret_key
        self.passphrase = passphrase
        
    
    def __call__(self, request):
        timestamp = str(time.time())
        message = timestamp + request.method + request.path_url + (request.body or '')
        message = message.encode('ascii')
        hmac_key = base64.b64decode(self.secret_key)
        signature = hmac.new(hmac_key, message, hashlib.sha256)
        signature_b64 = base64.b64encode(signature.digest()).decode('utf-8')

        request.headers.update({
            'CB-ACCESS-SIGN': signature_b64,
            'CB-ACCESS-TIMESTAMP': timestamp,
            'CB-ACCESS-KEY': self.api_key,
            'CB-ACCESS-PASSPHRASE': self.passphrase,
            'Content-Type': 'application/json'
        })
        return request
    
    #https://docs.gdax.com/?python#list-accounts
    def Get_Accounts(self):
        api_url = self.url + "/accounts"
        request = requests.get(api_url, auth=self)
        return request.json()

    #https://docs.gdax.com/?python#get-an-account
    def Get_Account(self, accountID):
        api_url = self.url + "/accounts/" + accountID
        request = requests.get(api_url,auth=self)
        return request.json()
    
    #https://docs.gdax.com/?python#get-account-history
    def Get_Account_History(self,accountID):
        api_url = self.url + "/accounts/" + accountID + "/ledger"
        entireHistory = []
        request = requests.get(api_url, auth=self)
        entireHistory.append(request.json())
        while("cb-after" in request.headers):
            api_url = self.url + "/accounts/" + accountID + "/ledger?after={" + str(request.headers["cb-after"]) + "}"
            request = requests.get(api_url, auth=self)
            entireHistory.append(request.json())
        return entireHistory

    #https://docs.gdax.com/?python#get-holds
    def Get_Holds(self,accountID):
        api_url = self.url + "/accounts/" + accountID + "/holds"
        allHolds = []
        request = requests.get(api_url, auth=self)
        allHolds.append(request.json())
        while("cb-after" in request.headers):
            api_url = self.url + "/accounts/" + accountID + "/holds?after={" + str(request.headers["cb-after"]) + "}"
            request = requests.get(api_url, auth=self)
            allHolds.append(request.json())
        return allHolds


    #https://docs.gdax.com/?python#orders
    def Market_Buy(self, productID, client_oid = None, stp = None, size=0, funds=0):
        api_url = self.url + '/orders'
        if size == 0 and funds ==0:
            return "Bad Market Buy"
        else:
            jsonData = {"product_id": productID, "client_oid":client_oid, "type":"market","side":"buy", "stp":stp, "size":size, "funds":funds  }
            jsonData = json.dumps(jsonData)
            request = requests.post(api_url,data=jsonData,auth=self)
            return request.json()
        
    def Market_Sell(self, productID, client_oid = None, stp = None, size=0, funds=0):
        api_url = self.url + '/orders'
        if size == 0 and funds ==0:
            return "Bad Market Sell"
        else:
            jsonData = {"product_id": productID, "client_oid":client_oid, "type":"market","side":"sell", "stp":stp, "size":size, "funds":funds  }
            jsonData = json.dumps(jsonData)
            request = requests.post(api_url,data=jsonData,auth=self)
            return request.json()
        
    #https://docs.gdax.com/?python#orders
    def Stop_Buy(self, productID, client_oid = None, stp = None, size=0, funds=0,stopPrice=0):
        api_url = self.url + '/orders'
        if size == 0 and funds ==0:
            return "Bad Stop Buy"
        else:
            if stopPrice == 0:
                return "Bad Stop Buy"
            else:
                jsonData = {"product_id": productID, "client_oid":client_oid, "type":"stop","side":"buy", "stp":stp, "size":size, "funds":funds, "price":stopPrice }
                jsonData = json.dumps(jsonData)
                request = requests.post(api_url,data=jsonData,auth=self)
                return request.json()
        
    def Stop_Sell(self, productID, client_oid = None, stp = None, size=0, funds=0,stopPrice=0):
        api_url = self.url + '/orders'
        if size == 0 and funds ==0:
            return "Bad Stop Sell"
        else:
            if stopPrice == 0:
                return "Bad Stop Buy"
            else:
                jsonData = {"product_id": productID, "client_oid":client_oid, "type":"market","side":"sell", "stp":stp, "size":size, "funds":funds, "price":stopPrice }
                jsonData = json.dumps(jsonData)
                request = requests.post(api_url,data=jsonData,auth=self)
                return request.json()    
        
    
    def Limit_Buy(self, productID, price=0, size=0, time_in_force="GTC",cancel_after = None, post_only=1, client_oid = None, stp = None,  ):
        api_url = self.url + '/orders'
        if price == 0 or size == 0:
            return "Bad Limit Buy"
        else:
            jsonData = {"product_id": productID, "price":price, "size":size, "time_in_force":time_in_force,"cancel_after":cancel_after,"post_only":post_only, "client_oid":client_oid, "type":"limit","side":"buy", "stp":stp}
            jsonData = json.dumps(jsonData)
            request = requests.post(api_url,data=jsonData,auth=self)
            return request.json()
 
 
    def Limit_Sell(self, productID, price=0, size=0, time_in_force="GTC",cancel_after = None, post_only=1, client_oid = None, stp = None,  ):
        api_url = self.url + '/orders'
        if price == 0 or size == 0:
            return "Bad Limit Buy"
        else:
            jsonData = {"product_id": productID, "price":price, "size":size, "time_in_force":time_in_force,"cancel_after":cancel_after,"post_only":post_only, "client_oid":client_oid, "type":"limit","side":"sell", "stp":stp}
            jsonData = json.dumps(jsonData)
            request = requests.post(api_url,data=jsonData,auth=self)
            return request.json()
    
    
    #https://docs.gdax.com/?python#list-orders
    def Get_Orders(self,productID,status=[]):
        api_url = self.url + "/orders"
        allOrders = []
        parameters= {}
        parameters["product_id"] = productID
        parameters["status"] = status
        request = requests.get(api_url, params=parameters ,auth=self)
        allOrders.append(request.json())
        while("cb-after" in request.headers):
            parameters["after"] = str(request.headers["cb-after"])
            request = requests.get(api_url, params=parameters ,auth=self)
            allOrders.append(request.json())
        return allOrders
    
    #https://docs.gdax.com/?python#get-an-order
    def Get_Order(self,orderID):
        api_url = self.url + '/orders/' + orderID
        request = requests.get(api_url, auth=self)
        return request.json()
    
    #https://docs.gdax.com/?python#cancel-an-order
    def Cancel_Order(self,orderID):
        api_url = self.url + '/orders/' + orderID
        request = requests.delete(api_url, auth=self)
        return request.json()
    
    #https://docs.gdax.com/?python#cancel-an-order
    def Cancel_All_Order(self,productID):
        api_url = self.url + '/orders/' + "?product_id={" + productID + "}"
        request = requests.delete(api_url, auth=self)
        return request.json()
    
    #https://docs.gdax.com/#fills
    def Get_Fills(self, orderID=None,productID=None):
        api_url = self.url + "/fills?"
        if orderID is not None:
            api_url += "order_id={" + orderID + "}&"
        if productID is not None:
            api_url += "product_id={" + productID + "}&"
            
        Fills = []
        parameters = {}
        request = requests.get(api_url, auth=self)
        Fills.append(request.json())
        while("cb-after" in request.headers):
            parameters["after"] = str(request.headers["cb-after"])
            request = requests.get(api_url, params=parameters ,auth=self)
            Fills.append(request.json())
        return Fills
        
        

