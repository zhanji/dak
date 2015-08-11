import socket

from utils import log
from node import Node
from rpc import Ping, Pong, Packet, PacketFactory

class Peer:
    def __init__(self, node, port):
      self.socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
      self.socket.bind(('', port))
      self.node = node

    def listen(self):
        log("Waiting for request...")

        while True:
            data, (reqAddr, reqPort) = self.socket.recvfrom(4096)

            packet = PacketFactory.packetfrombytes(data, self.node._id)
            packet.onreceive(self, reqAddr, reqPort)

            #update the bucket on every request
            reqType, reqIdentifier, reqNodeId = [row.decode() for row in data.split(b'\n')]
            contact = (reqNodeId, reqAddr, reqPort)
            self.node.addcontact(contact)

    def ping(self, address, port):
        ping = Ping(self.node._id)
        ping.send(self, address, port)

    def pong(self, address, port):
        pong = Pong(self.node._id)
        pong.send(self, address, port)

    def getsocket(self):
        return self.socket


