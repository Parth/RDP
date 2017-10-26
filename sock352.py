import binascii
import socket as syssocket
import struct
import sys

txPort = None
rxPort = None
HEADER_STRUCT = "!BBBBHHLLQQLL"
HEADER_SIZE = struct.calcsize(HEADER_STRUCT)

def init(UDPportTx,UDPportRx):
	txPort = UDPportTx
	rxPort = UDPportRx
	
class socket:
	def __init__(self): 
		self.ourSocket = syssocket.socket(syssocket.AF_INET, syssocket.SOCK_DGRAM)
		# TODO is there any reason a socket can't be created?
	
	def bind(self, address):
		self.ourSocket.bind(address)
		# TODO Does this need to return anything?
	
	def get_packet_header(self, version, flags, opt_ptr, protocol, checksum, source_port, dest_port, sequence_no, ack_no, window, payload_len):
		header_struct = struct.Struct(HEADER_STRUCT)
		return header_struct.pack(version, flags, opt_ptr, protocol, HEADER_SIZE, checksum, source_port, dest_port, sequence_no, ack_no, window, payload_len)

	def connect(self, address):  # fill in your code here 
		syn_header = self.get_packet_header(1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0)
		self.ourSocket.sendto(syn_header, address)
		# start timer
		#recv SYN ACK B
		#send ACK C
		#if there is error send header again
	
	def listen(self, backlog):
		pass

	#recv Syn A
	#send SYN ACK B
	# ACK C
	def accept(self):
		header = None
		while header is None: 
			data = self.ourSocket.recvfrom(HEADER_SIZE) 
			while data is not HEADER_SIZE:
				data = self.ourSocket.recvfrom(HEADER_SIZE) 

			unpacked = struct.unpack(HEADER_STRUCT, data)

			if unpacked[1] is 1:
				header = self.get_packet_header(1, 5, 0, 0, 0, 0, 0, 1, 1, 0, 0)


		(clientsocket, address) = (1,1)  # change this to your code 
		return (clientsocket,address)
	
	def close(self):   # fill in your code here 
		pass

	#create header
	#send data
	#start timer
	#if timeout, send same packet again
	#
	def send(self, buffer):
		bytessent = 0	 # fill in your code here 
		return bytesent 

	#recv packet
	#send right ACK
	def recv(self, nbytes):
		bytesreceived = 0	 # fill in your code here
		return bytesreceived 
