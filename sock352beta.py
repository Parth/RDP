import socket as syssock
import binascii
import struct
import sys
from collections import namedtuple
import time
from Queue import *
from random import *
import math
import packets.py

def init(UDPportTx, UDPportRx):  # initialize your UDP socket here

   	#init global socket for sending and receiving
    global global_socket
    global_socket = syssock.socket(syssock.AF_INET, syssock.SOCK_DGRAM)
    print "Global socket created"

    if UDPportTx < 1 or UDPportTx > 65535:
        UDPportTx = 27182

    if UDPportRx < 1 or UDPportRx > 65535:
        UDPportRx = 27182

class socket:
	#constructor for socket fields, need these fields to keep track of ack and sequence number and whether there is a socket connection
	def _init_(self):
		self.connected=False
		self.prev_ack=0
		self.next_ack=0
		self.init_seq=0
		self.next_seq=0

		return
	#n/a for this part of the project
	def bind (self, address):
		pass
	#creates a syn packet to be sent to initialize a connection
	def connect (self, address):

		#sets sequence and ack numbers to be referenced in the new syn packet
		self.init_seq=randint(0, 2**64)
		self.ack_no=0
		print "creating SYN Packet"
		#creates a new packet
		syn=new_packet()

		#specifies new packet as a syn packet
		syn.create_syn(self.init_seq)

		#packages the syn packet
		packsyn=syn.packPacket()
		print "Sending SYN Packet"
		#send out the syn packet to setup connection
		while True:

			#sends syn packet through global socket to address provided
			global_socket.sendto(packsyn, address)

			try:
				#sets timeout of .2 seconds, keep trying to send packet during this timeout

				#sets timeout for server to receive
				global_socket.settimeout(.2)

				#returns packet size in rpacket
				(rpacket, sender)=global_socket.recvfrom(packet_size)
			#fails if timeout exception
			except syssock.timeout:
				time.sleep(5)
			finally:

				print "Syn Packet sent successfully"
				#resets timer
				global_socket.settimeout(None)
		#retrieves packet header of 'syn' packet, packet header is the first 40 bytes of the packet as denoted by [:40]
		rec_packet=getpacketHeader(rpacket[:40])

		#checks flag to verify that it is indeed a SYN flag OR checks ack number to verify it is the sequence number +1 as denoted in class
		if (rec_packet.flags != 5 or rec_packet.ack_no != (syn.header.sequence_no + 1)):
			print "Bad SYN"
        	else:
        		#proper SYN, connect set to true, seq numbers set to proper values
        		self.connected= True
        		self.next_seq = rec_packet.ack_no
        		self.prev_ack = rec_packet.ack_no - 1
        		print "Connected"
        	return

    #n/a for part 1
    def listen (self, backlog):
    	pass

   	#called by server to accept the SYN packet, sending proper ACK, setting up new socket, and returning new socket for continued communication
    def accept(self):

    	while True:

    		try:
    			#sets timeout for receiving
    			global_socket.settimeout(.2)
    			(rpacket, sender)=global_socket.recvfrom(packet_size)
    			rec_packet=getpacketHeader(rec_packet[:40])
    		except syssock.timeout:
    			print "Socket timed out"
    		finally:
    			global_socket.settimeout(None)

    	#initial sequence number should be random between this range 0-2^64
    	self.init_seq=randint(0, 2**64)
    	#prev ack should be sequence number -1
    	self.prev_ack=rec_packet.sequence_no-1
    	#creates new packet of type ACK
    	ack=new_packet()
    	#sets flags of ACK pack, ACKING a SYN packet
    	ack.header.flags=ACK_VAL+SYN_VAL
    	ack.header.sequence_no=self.init_seq

    	#ack number is sequence number +1
    	ack.header.ack_no=rec_packet.sequence_no+1
    	#packages the ack packet
    	packed_ack=ack.packPacket()

    	#returns the number of bytes sent
    	bytessent=global_socket.sendto(packed_ack, sender)

    	#sets new socket
    	clientsocket=self
    	#returns new socket with address
    	return(clientsocket, sender)

    #function to close socket after finalizing communication
    def close(self):  # fill in your code here
        # send a FIN packet (flags with FIN bit set)
        # remove the connection from the list of connections
        #initializes FIN packet
        FIN = new_packet()
        FIN.header.flags = FIN_VAL
        packed_FIN = FIN.packPacket()
        global_socket.send(packed_FIN)
        self.connected = False
        self.prev_ack = 0
        self.next_seq = 0
        self.next_ack = 0
        self.init_seq = 0
        return

    #function to continue communication
    def send(self, buffer):
        bytessent = 0  # fill in your code here
        #assigns the data in buffer up until the 5000th byte to payload
        payload = buffer[:4098]
        #creates new packet of type payload
        data = new_packet()
        #assigns payload length
        data.header.payload_len = len(payload)
        #sets sequence and ack numbers
        data.header.sequence_no = self.next_seq
        data.header.ack_no = self.next_ack

        #assigns payload to the payload field of data packet
        data.payload = payload

        #packages the data packet
        packed_data = data.packPacket()

        while True:
            
            bytesSent = global_socket.send(packed_data)

            try:
                global_socket.settimeout(.2)
                (raw_packet, sender) = global_socket.recvfrom(header_len)
                rec_packet = packetHeader(raw_packet)
               
                if (rec_packet.flags != ACK_VAL or rec_packet.ack_no != (data_packet.header.sequence_no + 1)):
                    print "Wrong ACK"
                    #go back n protocol implemented here
                break

            except syssock.timeout:
                print "Socket Timed Out.."
                continue

            finally:
                global_socket.settimeout(None)
        #sets ack and sequence numbers of data packet
        self.next_seq= rec_packet.ack_no 
        self.prev_ack = rec_packet.ack_no - 1
        self.next_ack_no = rec_packet.ack_no + 1

        return bytesSent - header_len

    #function for server to receive
    def recv(self, nBytes):
      	#standard code of timeout and receive from functions
        while True:
            try:
                
                global_socket.settimeout(.2)
                rPack, sender = global_socket.recvfrom(5000)
                rec_packet_header = packetHeader(rPack[:40])
                
                if (rec_packet_header.flags > 0):
                    print "Not data packet"
                    if (rec_packet_header.flags == FIN_VAL):
                        global_socket.close()
                        break;

                else:
                    break

            except syssock.timeout:
                print "Socket timed out recieving"

            finally:
                global_socket.settimeout(None)

        self.next_seq = rec_packet.ack_no
        self.prev_ack= rec_packet.ack_no - 1
        self.next_ack = rec_packet.ack_no + 1

        
        #payload is now everything after the 40th byte of the received packet
        payload = rPack[40:] #(40+bytessent)?
       



        ack = packet()
        ack.create_ack(rec_packet)
        packed_ack = ack.packPacket()
        global_socket.sendto(packed_ack, sender)

        return payload
