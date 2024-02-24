import requests

class Client:
	#constructor, takes a message catalog
    def __init__(self, c, h="http://localhost:5000/", oc="http://localhost:5000/", t=5):
        self.catalog = c
        self.hospital_address = h
        self.other_client_address = oc

        self.run = False #loop is running when true
        self.proximity = False #true if the other client is close


	#send an I said message to the other client
    def say_something(self):
        msg = self.catalog.generateMessage() #generate message, returns string
        r = requests.post(self.other_client_address + msg)
        if r.status_code != 200:
            print("failed")
            self.catalog.messages = self.catalog.messages[:-1] #removing last element from tab
            self.catalog.messages.deleteXMLMessage(msg)  #removing from XML cartalog

	#add to catalog all messages from hospital
    def get_covid(self):
        r = requests.get(self.hospital_address + "they-said")
        self.catalog.importData(r.json(),1) #import data from hospital
        if self.catalog.quarantine():
            print("\n ATTENTION POSSIBILITE DE COVID \n")
        else:
            print("\n Pas de risque de covid \n")


	#send to hospital the list of “I said” messages
    def send_history(self):
        self.catalog.purge() #removing messages older than 14 days
        data = self.catalog.exportData() #exports I said messages without param
        requests.post(self.hospital_address + 'they-said',json=data)
        print("\n vous venez de déclarer un cas de covid \n")
            
            
    def loop(self):
        #sending message to other client
        if self.proximity:
            self.say_something() 
        
        
    #returns true if the 3 applications are ready
    def allClientsReady(self):
        res = False
        r1 = requests.get(self.hospital_address) #requesting hospital index
        r2 = requests.get(self.other_client_address) #other client index
        if r1.status_code != 200: #hospital not running
            res = False 
        elif r1.status_code == 200: #request successful = hospital running 
            if r2.status_code != 200:
                res = False
            elif r2.status_code == 200: #other client is running
                res = True
                self.run = True
            else:
                print("allClientsReady problem")
        else:
            print("allClientsReady problem")
        return res
        
    #in final application proximity switch must be calculated using gps location
    #so far we inform the other client that we changed proximity setting
    def toggleProximity(self, origin = False):
        if self.proximity:
            self.proximity = False
            print("\n Il n'y a plus d'utilisateur à proximité \n")
        else:
            self.proximity = True
            print("\n Un utilisateur est à proximité \n")
        
        ''' #this two lines need to be enables to test with 3 different computers
        if origin: #inform the other client if we initiated the change
            requests.get(self.other_client_address+"proximity")
        '''
        
    
    
    
        
        
        
        
        