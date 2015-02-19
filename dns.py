#!/home/mattjm/bin/python3
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
    apiKey='ABC'
    #specify domain name here
    domainName = 'domain.example.com'
    #specify password below (NOT A PASSWORD YOU USE FOR ANYTHING ELSE)
    #This is just for this tool
    myPass = 'oneseventhree'
    #-----USER EDITABLE ABOVE-----
    
    #this lets a web browser display the output of the program
    print("Content-type: text/html\n\n")
    
    #the API URL shouldn't change, but if it does you can change it here
    apiURL = 'https://api.dreamhost.com/'
    
   
    #get the current date....ignore the 2015-01-01....for some reason
    #a date is required to instantiate the class.  today() sets it to the
    #current date
    myDate = datetime.datetime(year=2015,month=1,day=1).today()
    
    
    #instantiate the class that handles the HTTP calls
    myDAL = httpcalls.DAL(baseURL=apiURL)
    
    #Magic to obtain external IP address
    currentlocalIP=os.environ['REMOTE_ADDR']
    print(currentlocalIP)
    #Get password from query string via server variables
    myData = cgi.FieldStorage()
    givenPass = myData.getfirst('password','')
    #check password
    if givenPass != myPass:
        print('Unauthorized')
        exit()

    
    
    #This dictionary will be turned into a querystring by the requests library.  It contains
    #all the required parameters for the API call
    myListQuery = {'key':apiKey,
              'cmd':'dns-list_records',
              'format':'json'}
    
    #get the list of current records
    mydhRecords = myDAL.rqGET(values=myListQuery)
    
    #load the json response from DH  into a dictionary object
    allRecords = json.loads(mydhRecords.text)
    
    #create some variables--we'll set them in the loop that follows
    shouldChange = True
    oldIP = ''
    recordExists = False 
    #iterate through all records
    for x in allRecords['data']:
        #if we find the record we want, let's do some stuff with it
        if x['record'] == domainName and not recordExists:
            #Let's make a note that the record exists
            recordExists = True
            #check the IP address in the record against the one we have right now
            if x['value'] == currentlocalIP:
                #we don't need to change it if it's the same
                shouldChange = False
                print('IP has not changed--no update needed.')
            else:
                #If they aren't the same we need to know the old IP to delete the outdated record
                #remember shouldChange was true when we created it so we don't need to change the flag
                oldIP = x['value']
                print('IP has changed--will proceed with update')
            
            
    #Only do the following if the IP isn't the same as it was before
    if shouldChange:
    
        #delete existing record
        
        #This dictionary will be turned into a querystring by the requests library.  It contains
        #all the required parameters for the API call
        myoldrecord = {'record':domainName,
                       'type':'A',
                       'value':oldIP,
                       'key':apiKey,
                       'cmd':'dns-remove_record',
                       'format':'json'}
        
        
        #delete the outdated record if it exists
        if recordExists:
            myrecordedit = myDAL.rqGET(values=myoldrecord)
            #print the results
            print(myrecordedit.text)
        
        #Create new record
        #This dictionary will be turned into a querystring by the requests library.  It contains
        #all the required parameters for the API call
        mynewrecord = {'record':'pytest.mattjm.com',
                       'type':'A',
                       'value':currentlocalIP,
                       'comment' : 'updated by mattjm python script at ' + str(myDate), 
                       'key':apiKey,
                       'cmd':'dns-add_record',
                       'format':'json'}
        
       
        
        #add the record
        myrecordedit = myDAL.rqGET(values=mynewrecord)
        #print the results
        print(myrecordedit.text)
   
        

if __name__ == '__main__':  main()
