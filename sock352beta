import socket as syssock
import binascii
import struct
import sys
from collections import namedtuple
import time
from Queue import *
from random import *
import math

HEADER_STRUCT = "!BBBBHHLLQQLL"
HEADER_SIZE = struct.calcsize(HEADER_STRUCT)

SYN_VAL = 0x1
FIN_VAL = 0x2
ACK_VAL = 0x4
RESET_VAL = 0x8
OPTION_VAL = 0xA0

packet_size=5000

class packHeader:
    def __init__(self, theHeader=None):
        self.header_struct = struct.Struct(HEADER_STRUCT)

        if (theHeader is None):
            self.flags = 0
            self.version = 1
            self.opt_ptr = 0
            self.protocol = 0
            self.checksum = 0
            self.sequence_no = 0
            self.source_port = 0
            self.ack_no = 0
            self.dest_port = 0
            self.window = 0
            self.payload_len = 0
        else:
            self.unpackHeader(theHeader)

    #Returns a packed header object
    def getPacketHeader(self):
        return self.header_struct.pack(self.version, self.flags, self.opt_ptr, self.protocol, struct.calcsize(HEADER_STRUCT), self.checksum, self.source_port, self.dest_port, self.sequence_no, self.ack_no, self.window, self.payload_len)

    #Returns an unpacked header
    def unpackHeader(self, theHeader):
        if len(theHeader) < 40:
            print ("Invalid Header")
            return -1

        header_arr = self.header_struct.unpack(theHeader)
        self.version = header_array[0]
        self.flags = header_array[1]
        self.opt_ptr = header_array[2]
        self.protocol = header_array[3]
        self.header_len = header_array[4]
        self.checksum = header_array[5]
        self.source_port = header_array[6]
        self.dest_port = header_array[7]
        self.sequence_no = header_array[8]
        self.ack_no = header_array[9]
        self.window = header_array[10]
        self.payload_len = header_array[11]
        return header_arr

    #Creates a packet
class new_packet:
    def __init__(self, header=None, payload=None):
        if header is None:
            self.header = packetHeader()
        else:
            self.header = header
        if payload is None:
            self.payload = None
        else:
            self.payload = payload
            self.header.payload_len = len(self.payload)
        pass
    #Packs the packetheader and payload
    def packPacket(self):
        packed_header = self.header.packPacketHeader()

        if (self.payload is None):
            packed_packet = packed_header
        else:
            packed_packet = packed_header + self.payload

        return packed_packet

    #Creates an ack packet
    def create_ack(self, rHeader):
        self.header.ack_no = rHeader.sequence_no + rHeader.payload_len
        self.header.sequence_no = rHeader.ack_no + 1;
        self.header.flags = ACK_VAL;
    #Creates a SYN packet
    def create_syn(self, seq_num):
        self.header.flags = SYN_VAL
        self.header.sequence_no = seq_num

def init(UDPportTx, UDPportRx):  # initialize your UDP socket here
    print ("Inside Global Init...........")
    global global_socket
    global_socket = syssock.socket(syssock.AF_INET, syssock.SOCK_DGRAM)


    if UDPportTx < 1 or UDPportTx > 65535:
        UDPportTx = 27182

    if UDPportRx < 1 or UDPportRx > 65535:
        UDPportRx = 27182

class socket:

	def _init_(self):
		self.connected=False
		self.prev_ack=0
		self.next_ack=0
		self.init_seq=0
		self.next_seq=0

		return

	def bind (self, address):
		pass

	def connect (self, address):
		self.init_seq=randint(0, 2**64)
		self.ack_no=0

		syn=new_packet()
		syn.create_syn(self.init_seq)
		packsyn=syn.packPacket()

		while True:
			global_socket.sendto(packsyn, address)

			try:
				global_socket.settimeout(.2)
				(rpacket, sender)=global_socket.recvfrom(packet_size)
			except syssock.timeout
			finally:
				global_socket.settimeout(None)

		rec_packet=getpacketHeader(rpacket[:40])
		if (rec_packet.flags != 5 or
                    rec_packet.ack_no != (syn.header.sequence_no + 1)):
            print "Bad SYN"
        else:
            self.connected= True
            self.next_seq = rec_packet.ack_no
            self.prev_ack = rec_packet.ack_no - 1
            print "Connected"
        return

    def listen (self, backlog):
    	pass

    def accept(self):

    	while True:

    		try:
    			global_socket.settimeout(.2)
    			(rpacket, sender)=global_socket.recvfrom(packet_size)
    			rec_packet=getpacketHeader(rec_packet[:40])
    		except syssock.timeout
    			print "Socket timed out"
    		finally:
    			global_socket.settimeout(None)

    	self.init_seq=randint(0, 2**64)
    	self.prev_ack=rec_packet.sequence_no-1
    	ack=new_packet()
    	ack.header.flags=ACK_VAL+SYN_VAL
    	ack.header.sequence_no=self.init_seq
    	ack.header.ack_no=rec_packet.sequence_no+1

    	packed_ack=ack.packPacket()

    	bytessent=global_socket.sendto(packed_ack, sender)

    	clientsocket=self

    	return(clientsocket, sender)

    def close(self):  # fill in your code here
        # send a FIN packet (flags with FIN bit set)
        # remove the connection from the list of connections

        FIN = packet()
        FIN.header.flags = FIN_VAL
        packed_FIN = FIN.packPacket()
        global_socket.send(packed_FIN)
        self.connected = False
        self.prev_ack = 0
        self.next_seq = 0
        self.next_ack = 0
        self.init_seq = 0
        return

    def send(self, buffer):
        bytessent = 0  # fill in your code here
        payload = buffer[:4098]
        data = packet()
        data.header.payload_len = len(payload)
        data.header.sequence_no = self.next_seq
        data.header.ack_no = self.next_ack
        data.payload = payload

        packed_data = data.packPacket()

        while True:
            
            bytesSent = global_socket.send(packed_data)

            try:
                global_socket.settimeout(.2)
                (raw_packet, sender) = global_socket.recvfrom(header_len)
                rec_packet = packetHeader(raw_packet)
               
                if (rec_packet.flags != ACK_VAL or
                            rec_packet.ack_no != (
                            data_packet.header.sequence_no + 1)):
                    print "Wrong ACK"
                break

            except syssock.timeout:
                print "Socket Timed Out.."
                continue

            finally:
                global_socket.settimeout(None)

        self.next_seq= rec_packet.ack_no 
        self.prev_ack = rec_packet.ack_no - 1
        self.next_ack_no = rec_packet.ack_no + 1

        return bytesSent - header_len


    def recv(self, nBytes):
      
        while True:
            try:
                
                global_socket.settimeout(.2)
                rPack, sender = global_socket.recvfrom(5000)
                rec_packet = packetHeader(rPack[:40])
                
                if (rec_packet.flags > 0):
                    print "Not data packet"
                    if (recieved_packet_header.flags == FIN_VAL):
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

        

        payload = rPack[40: (40+nBytes)]
       



        ack = packet()
        ack.create_ack(rec_packet)
        packed_ack = ack.packPacket()
        global_socket.sendto(packed_ack, sender)

        return payload



