'''
Created on Apr 1, 2014

This is the data access layer.  

@author: mattjm
'''
import json
import sys
import getopt
import requests
from datetime import *

class DAL(object):
    
    #set cert location and baseURL when class is instantiated
    def __init__ (self, baseURL):
        """Data Abstraction Layer"""
        #self.certfile = certfile
        self.baseURL = baseURL
        
       
    
    '''Given a path and payload, performs a PUT and returns the http response.  Path will be appended to the BaseURL.  Payload must be JSON.  '''
        
    

    
    def rqPUT(self, path, payload = '', PayloadType = 'json'):
        """"""
       
        print(path)
        if PayloadType == 'json':
            
            jsonPayload = json.dumps(payload)
            #content-length here is a dummy value--requests library will set it to the proper length for the payload
            myHeaders = {'content-type': 'application/json', 'content-length':'2'}
            myResponse = requests.put(self.baseURL + path, verify=False, cert=self.certfile, headers=myHeaders, data=jsonPayload)
            
        if PayloadType == 'querystring':
            myHeaders = {}
            myResponse = requests.put(self.baseURL + path, verify=False, cert=self.certfile, headers=myHeaders)
        print('DEBUG URL:' + self.baseURL + path) 
        
        myResponse.close()
        return myResponse
    
    '''Given a path and payload, performs a POST and returns the http response.  Path will be appended to the BaseURL.  Payload must be JSON.  '''
    def rqPOST(self, path, values):
        """"""
        
       
        myResponse = requests.post(self.baseURL, verify=False, params=values)
        print(myResponse.request.url)
        print(myResponse.request.headers)
        print('DEBUG URL:' + self.baseURL + path) 
        myResponse.close()
        return myResponse
    
    '''Given a path, performs a GET and returns the http response.  Path must will be appended to the BaseURL, and must contain the identifier in the proper format.'''
    def rqGET(self, values):
        myResponse = requests.get(self.baseURL, verify=False, params=values)
        #print(myResponse.request.headers)
        #print(myResponse.request.url)
        #print('DEBUG URL:' + self.baseURL) 
        myResponse.close()
        return myResponse
    
    def rqDELETE(self, path):
        
        print('attempting delete of ' + self.baseURL + path)
        myResponse = requests.delete(self.baseURL + path, verify=False, cert=self.certfile)
        print(myResponse.text)
        
        print('DEBUG URL:' + self.baseURL + path) 
        myResponse.close()
        return myResponse
    
    def rqGETjson(self, path, payload):
        myResponse = requests.get(self.baseURL + path, verify=False, cert=self.certfile)
        #print(myResponse.headers)
        
        print('DEBUG URL:' + self.baseURL + path) 
     
        jsonPayload = json.dumps(payload)
        #content-length here is a dummy value--requests library will set it to the proper length for the payload
        myHeaders = {'content-type': 'application/json', 'content-length':'2'}
        myResponse = requests.get(self.baseURL + path, verify=False, cert=self.certfile, headers=myHeaders, data=jsonPayload)
        myResponse.close()
        return myResponse