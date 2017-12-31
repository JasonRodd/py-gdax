'''
@author: Jason Rodd
Used to get market data from gdax.
'''

import requests
import json
import datetime
import time;

class Market():
    
    def __init__(self):
        self.url = "https://api.gdax.com"
    
    #https://docs.gdax.com/?python#get-products
    def Get_Products(self):
        api_url = self.url + "/products"
        request = requests.get(api_url, params=None)
        return request.json()

    #https://docs.gdax.com/?python#get-product-order-book
    def Get_Product_Order_Book(self,productID,level=1):
        api_url = self.url + "/products/" + productID + "/book"
        
        if level > 3 or level < 1:
            level = 1 
            
        parameters = {"level": level}
        request = requests.get(api_url, params=parameters)
        return request.json()
    
    #https://docs.gdax.com/?python#get-product-ticker
    def Get_Product_Ticker(self,productID):
        api_url = self.url + "/products/"+ productID + "/ticker"
        request = requests.get(api_url, params=None)
        return request.json()
    
    #https://docs.gdax.com/?python#get-trades
    def Get_Trades(self,productID):
        api_url = self.url + "/products/" + productID + "/trades"
        request = requests.get(api_url, params=None)
        return request.json()
    
    #https://docs.gdax.com/?python#get-historic-rates
    def Get_Historic_Rates(self,productID, startDate, endDate, granularity=60):
        api_url = self.url + "/products/" + productID + "/candles"
        
        Grains = [60, 300, 900, 3600, 21600, 86400]
        if granularity not in Grains:
            granularity = 60
        
        '''
            startDate and endDate are kept epoch
            endDate - startDate = timeDelta (in seconds)
            gdax only allows for 200 buckets: thus each granularity level has a defined max timeframe
            if timeDelta > defined max timeframe we CANCEL this call attempt
            we then convert epoch into ISO 1806 to pass to gdax
        '''
        timeDelta = endDate - startDate
        timeFrames = {60:12000,300:60000,900:180000,3600:720000,21600:4320000,86400:17280000}
        timeFrame = timeFrames[granularity]
        
        if timeDelta > timeFrame:
            print(timeDelta)
            return "timeDelta to large"
        
        isoStart = datetime.datetime.utcfromtimestamp(startDate).isoformat()
        isoEnd = datetime.datetime.utcfromtimestamp(endDate).isoformat()
        
        parameters = {"start": isoStart, "end": isoEnd, "granularity": granularity}   
        request = requests.get(api_url, params=parameters)
        return request.json()

    #https://docs.gdax.com/?python#get-24hr-stats
    def Get_24hr_Stats(self,productID):
        api_url = self.url + "/products/" + productID + "/stats"
        request = requests.get(api_url, params=None)
        return request.json()
    
    #https://docs.gdax.com/?python#currencies
    def Get_Currencies(self):
        api_url = self.url + "/products/stats"
        request = requests.get(api_url, params=None)
        return request.json()

    def Get_Time(self):
        api_url = self.url + "/time"
        request = requests.get(api_url, params=None)
        return request.json()


      