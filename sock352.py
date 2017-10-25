import binascii
import socket as syssock
import struct
import sys

# these functions are global to the class and
# define the UDP ports all messages are sent
# and received from

def init(UDPportTx,UDPportRx):   # initialize your UDP socket here 
    pass 
    
class socket:
    
    def __init__(self):  # fill in your code here 
        return
    
    def bind(self,address):
        return 

    #bind
    #Create SYN Header
    # start timer
    #recv SYN ACK B
    #send ACK C
    #if there is error send header again
    def connect(self,address):  # fill in your code here 
		pass
    
    def listen(self,backlog):
		pass

	#recv Syn A
	#send SYN ACK B
	# ACK C
    def accept(self):
        (clientsocket, address) = (1,1)  # change this to your code 
        return (clientsocket,address)
    
    def close(self):   # fill in your code here 
		pass

    #create header
    #send data
    #start timer
    #if timeout, send same packet again
    #
    def send(self,buffer):
        bytessent = 0     # fill in your code here 
        return bytesent 

	#recv packet
	#send right ACK
    def recv(self,nbytes):
        bytesreceived = 0     # fill in your code here
        return bytesreceived 
