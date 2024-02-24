from datetime import datetime
from datetime import timedelta

#for generation of messages
import random
import string

class Message:
     
    #three different types
    #0 : i said message
    #1 : I heard message
    #2 : message from hospital
    #three different constructors :
    #Message(String) : message already exists in XML catalog
    #Message(int) : new "I said" message
    #Message(String,int) : new "I heard" message or message from hospital
    def __init__(self,*args):
        self.type = 0
        self.date = ""
        self.content = ""
        
        #existing message
        if len(args)==1 and isinstance(args[0],str):
            self.retrieveAttributes(args[0])
        #new I said
        elif len(args)==1 and isinstance(args[0],int):
            self.type = 0
            self.date = datetime.now()
            self.content = self.generateRandomContent(8) #random string (l=8)
        #new I heard or hospital
        elif len(args)>1:
            if args[1] == 1: #message from other client
                self.type = args[1]
                self.date = datetime.now()
                self.content = args[0]
            else:
                self.retrieveAttributes(args[0]) #loading content and date
                self.type = 2 #updating origin to hospital
        else:
            print("oh oh")
            
        
    def generateRandomContent(self,length):
        res=""
        for x in range(length):
            res += str(random.choice(string.ascii_letters + string.digits))
        return res
    
    def retrieveAttributes(self,s):
        c = 0
        attributes = ["","",""]
        for i in range(len(s)):
            if s[i] == ';':
                c+=1
            else:
                attributes[c] = attributes[c] + str(s[i])
                
        self.type = int(attributes[0])
        self.date = datetime.strptime(attributes[1],"%d-%m-%Y")
        self.content = attributes[2]
            
                
    #check if message is older than a given number of day   
    def olderThan(self,d):
        res = False
        delay = timedelta(days=d)
        if self.date < datetime.now()-delay:
            res = True
        return res

	#a method to convert the object to string data
    def __str__(self):
        timestampStr = self.date.strftime("%d-%m-%Y")
        
        #message : type;date;content
        return str(self.type)+";"+timestampStr+";"+self.content
	


