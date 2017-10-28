import binascii
import socket as syssocket
import struct
import sys
import datetime import datetime
import random import randint

txPort = None
rxPort = None
HEADER_STRUCT = "!BBBBHHLLQQLL"
HEADER_SIZE = struct.calcsize(HEADER_STRUCT)

def init(UDPportTx,UDPportRx):
	txPort = UDPportTx
	rxPort = UDPportRx
	
class socket:

	def __init__(self, peer_address=None): 
		self.ourSocket = syssocket.socket(syssocket.AF_INET, syssocket.SOCK_DGRAM)

		if peer_address is not None: 
			self.peer_address = peer_address
			self.connected = True
	
	def bind(self, address):
		self.ourSocket.bind(address)
		# TODO Does this need to return anything?
	
	def get_packet_header(self, version, flags, opt_ptr, protocol, checksum, source_port, dest_port, sequence_no, ack_no, window, payload_len):
		header_struct = struct.Struct(HEADER_STRUCT)
		return header_struct.pack(version, flags, opt_ptr, protocol, HEADER_SIZE, checksum, source_port, dest_port, sequence_no, ack_no, window, payload_len)

	def send_syn(self, address):
		syn = self.get_packet_header(1, 1, 0, 0, 0, 0, 0, 0, randint(0, 2**32), 0, 0)
		self.ourSocket.sendto(syn, address)

	def connect(self, address):  # fill in your code here 
		if not self.connected:
			self.peer_address = address

			startTime = datetime.now()
			timeElapsed = datetime.now() - startTime

			final_ack = None
			while final_ack is None: 
				send_syn(address)
				while timeElapsed.microseconds < 200000:
					timeElapsed = datetime.now() - timeElapsed
					(data, address) = self.ourSocket.recvfrom(HEADER_SIZE)
					syn_ack = struct.unpack(HEADER_STRUCT, data)

					if syn_ack[1] is 5:
						final_ack = self.get_packet_header(1, 4, 0, 0, 0, 0, 0, unpacked[9]+1, 1, 0, 0)

			self.ourSocket.sendto(final_ack, address)
			self.connected = True
		else:
			print("error, socket already connected")
	
	def listen(self, backlog):
		pass

	#recv Syn A
	#send SYN ACK B
	# ACK C
	def accept(self):
		header = None
		address = None
		while header is None:
			(data, address) = self.ourSocket.recvfrom(HEADER_SIZE)
			unpacked = struct.unpack(HEADER_STRUCT, data)

			if unpacked[1] is 1:
				sequence_number = randint(0, 2**32)
				header = self.get_packet_header(1, 5, 0, 0, 0, 0, 0, sequence_number, unpacked[8]+1, 0, 0)

		self.ourSocket.sendto(header, address)

		clientsocket = None
		while clientsocket is None:
			(data, address2) = self.ourSocket.recvfrom(HEADER_SIZE)

			if address2 == address:
				unpacked = struct.unpack(HEADER_STRUCT, data)

				if unpacked[1] is 4:
					clientsocket = self.socket(address=address)
			
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
