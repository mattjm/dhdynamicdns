#!/home/username/local/bin/python

import json
import httpcalls
import datetime
import os
import cgi
#import cgitb

def main():
    
    #cgitb prints debugging information--generally leave off.  
    #cgitb.enable()
    
    #-----USER EDITABLE BELOW-----
    #Specify API Key here
    apiKey=u'ABC'
    #specify domain name here
    domainName = u'sub.domain.com'
    #specify password below (NOT A PASSWORD YOU USE FOR ANYTHING ELSE)
    #This is just for this tool
    myPass = u'oneseventhree'
    #-----USER EDITABLE ABOVE-----
    
    #this lets a web browser display the output of the program
    print u"Content-type: text/html\n\n"
    print  
    #the API URL shouldn't change, but if it does you can change it here
    apiURL = u'https://api.dreamhost.com/'
    
   
    #get the current date....ignore the 2015-01-01....for some reason
    #a date is required to instantiate the class.  today() sets it to the
    #current date
    myDate = datetime.datetime(year=2015,month=1,day=1).today()
    
    
    #instantiate the class that handles the HTTP calls
    myDAL = httpcalls.DAL(baseURL=apiURL)
    
    #Magic to obtain external IP address
    currentlocalIP=os.environ[u'REMOTE_ADDR']
    print currentlocalIP
    #Get password from query string via server variables
    myData = cgi.FieldStorage()
    givenPass = myData.getfirst(u'password',u'')
    #check password
    if givenPass != myPass:
        print u'Unauthorized'
        exit()

    
    
    #This dictionary will be turned into a querystring by the requests library.  It contains
    #all the required parameters for the API call
    myListQuery = {u'key':apiKey,
              u'cmd':u'dns-list_records',
              u'format':u'json'}
    
    #get the list of current records
    mydhRecords = myDAL.rqGET(values=myListQuery)
    
    #load the json response from DH  into a dictionary object
    allRecords = json.loads(mydhRecords.text)
    
    #create some variables--we'll set them in the loop that follows
    shouldChange = True
    oldIP = u''
    recordExists = False 
    #iterate through all records
    for x in allRecords[u'data']:
        #if we find the record we want, let's do some stuff with it
        if x[u'record'] == domainName and not recordExists:
            #Let's make a note that the record exists
            recordExists = True
            #check the IP address in the record against the one we have right now
            if x[u'value'] == currentlocalIP:
                #we don't need to change it if it's the same
                shouldChange = False
                print u'IP has not changed--no update needed.'
            else:
                #If they aren't the same we need to know the old IP to delete the outdated record
                #remember shouldChange was true when we created it so we don't need to change the flag
                oldIP = x[u'value']
                print u'IP has changed--will proceed with update'
            
            
    #Only do the following if the IP isn't the same as it was before
    if shouldChange:
    
        #delete existing record
        
        #This dictionary will be turned into a querystring by the requests library.  It contains
        #all the required parameters for the API call
        myoldrecord = {u'record':domainName,
                       u'type':u'A',
                       u'value':oldIP,
                       u'key':apiKey,
                       u'cmd':u'dns-remove_record',
                       u'format':u'json'}
        
        
        #delete the outdated record if it exists
        if recordExists:
            myrecordedit = myDAL.rqGET(values=myoldrecord)
            #print the results
            print myrecordedit.text
        
        #Create new record
        #This dictionary will be turned into a querystring by the requests library.  It contains
        #all the required parameters for the API call
        mynewrecord = {u'record':u'pytest.mattjm.com',
                       u'type':u'A',
                       u'value':currentlocalIP,
                       u'comment' : u'updated by mattjm python script at ' + unicode(myDate), 
                       u'key':apiKey,
                       u'cmd':u'dns-add_record',
                       u'format':u'json'}
        
       
        
        #add the record
        myrecordedit = myDAL.rqGET(values=mynewrecord)
        #print the results
        print myrecordedit.text
   
        

if __name__ == u'__main__':  main()
