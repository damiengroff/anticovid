#!/usr/bin/env python3
from message import Message
import xml.dom.minidom as minidom

class MessageCatalog:
	#constructor, loads the messages (if there are any)
    def __init__(self, filepath):
        self.messages = []
        self.__file = minidom.parse(filepath)
        
        #retrieve existing messages from XML file
        self.retrieveXMLMessages()
        
    
    #create messages from XML files and storing in object's attribute
    def retrieveXMLMessages(self):
        m = self.__file.getElementsByTagName("message")
        for i in range(len(m)):
            self.messages.append(Message(m[i].firstChild.nodeValue))
      
            
    #remove element from XML catalog (based on message string)
    def deleteXMLMessage(self,msg):
        m = self.__file.getElementsByTagName("messages")
        i = 1
        while i < len(m[0].childNodes):
            if m[0].childNodes[i].firstChild.nodeValue == msg:
                m[0].removeChild(m[0].childNodes[i])
                m [0].removeChild(m[0].childNodes[i-1]) #remove line break
                i+=len(m[0].childNodes) #escape loop
            else:
                i+=2 #incremant by 2 to avoid line breaks
                
        #print(self.__file.toxml())
    
    
    #add element in XML catalog (content as parameter)
    def addXMLMessage(self,msg):
        node = self.__file.createElement("message")
        node.appendChild(self.__file.createTextNode(msg))
        
        m = self.__file.getElementsByTagName("messages")
        m[0].appendChild(node)
        m[0].appendChild(self.__file.createTextNode("\n")) #line break
       
        #print(self.__file.toxml())
     
        
    #method to create an I said message (return its content to client)
    def generateMessage(self):
        message = Message(0) #I said type
        self.messages.append(message)
        self.addXMLMessage(message.__str__())
        return message.content #message to be sent to host
    
    #create an I heard message, parameter addressed by client app
    def addHeardMessage(self,msg):
        message = Message(msg,1) #I heard type
        self.messages.append(message)
        self.addXMLMessage(message.__str__())

    #returns true if message is in catalog (from its str())
    def isInCatalog(self,msg):
        res = False
        for i in range(len(self.messages)):
            if self.messages[i].__str__() == msg:
                res = True
        return res

    #remove outdated messages, age in days
    def purge(self, age = 14):   
        i=0
        l=len(self.messages)
        
        while i<l:
            if self.messages[i].olderThan(age):
                self.deleteXMLMessage(self.messages[i].__str__())
                self.messages.remove(self.messages[i])
                l-=1 #adjusting table length
                i-=1
            i+=1
            
    #export json messages by type (default : i said, hospital usecase ty = 2)
    def exportData(self,ty=0):
        res = "[" #result string, json 
        
        #retrieving all desired type messages
        for i in range(len(self.messages)):
            if self.messages[i].type == ty:
                res += "\n"
                res += "{\"msg\":\""+self.messages[i].__str__()+"\"},"
        
        res = res[:-1] #removing last coma
        res += "\n]"
        return res
    
    #generate Message objects and write on xml file
    #from json data as parameter        
    def importData(self,data, origin = 0):
        for i in data:
            self.messages.append(Message(i["msg"],2)) #adding msg to catalog
            self.addXMLMessage(self.messages[-1].__str__())
            #possible upgrade : before importing a message, make sure it does
            # not alreay exists

    #returns true if client should quarantine
    #count matches found between types 1 and 2
    def quarantine(self, contacts = 10):
        heard = []
        hospital = []
        
        #self.purge()
        
        for i in range(len(self.messages)):
            if self.messages[i].type == 1:
                heard.append(self.messages[i])
            if self.messages[i].type == 2:
                hospital.append(self.messages[i])
                
        matches = 0
        
        for i in range(len(heard)):
            for j in range(len(hospital)):
                if heard[i].content == hospital[j].content:
                    matches+=1
                    
        if matches>=contacts:
            return True
        else:
            return False
            
    def __str__(self):
        return self.__file.toxml()
    
    def save(self):
        with open("msgxml.xml", "w") as output_xml:
            self.__file.writexml(output_xml)

#will only execute if this file is run
if __name__ == "__main__":
	
    m = MessageCatalog("msgxml.xml")
    #print(m.messages[0])
    #m.addXMLMessage("test")
    #m.addXMLMessage("test") 
    #m.deleteXMLMessage(m.messages[2].__str__())
    #m.generateMessage()
    #.purge()
    #m.generateMessage()
    #m.addHeardMessage("aaaaaaaa")
    #m.importData(["2;14/11/2021;aaaaaaaa","2;14/11/2021;bbbbbbbb"])
    #print(m.quarantine(2))
    #print(m.exportData())
    print(m)