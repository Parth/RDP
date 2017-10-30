import socket as syssock
import binascii
import struct
import sys
from collections import namedtuple
import time
from Queue import *
from random import *
import math

#set struct format and size
HEADER_STRUCT = "!BBBBHHLLQQLL"
HEADER_SIZE = struct.calcsize(HEADER_STRUCT)

#set header flags
SYN_VAL = 0x1
FIN_VAL = 0x2
ACK_VAL = 0x4
RESET_VAL = 0x8
OPTION_VAL = 0xA0

#set packet size
packet_size=5000


#header object for referencing
class packHeader:
    def __init__(self, theHeader=None):
        self.header_struct = struct.Struct(HEADER_STRUCT)

        #constructor for header fields
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
        	#unpack header for receive function
            self.unpackHeader(theHeader)

    #Returns a packed header object
    def getPacketHeader(self):
        return self.header_struct.pack(self.version, self.flags, self.opt_ptr, self.protocol, struct.calcsize(HEADER_STRUCT), self.checksum, self.source_port, self.dest_port, self.sequence_no, self.ack_no, self.window, self.payload_len)

    #Returns an unpacked header
    '''def unpackHeader(self, theHeader):
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
        return header_arr'''

#packet object
class new_packet:
    def __init__(self, header=None, payload=None):
    	#constructor for packet fields, differs from header by adding payload
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
    #Packs the packetheader and payload and combines them into one packet object
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