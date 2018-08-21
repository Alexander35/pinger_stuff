import socket
import struct
import ctypes, sys
import asyncio
import datetime 
from async_timeout import timeout

class Ping:
	def __init__(self, ip_list, timeout):
		self.ip_list = ip_list
		self.available_list = []
		self.timeout = timeout
		
	def checksum(self, source_string):
		""" this func from https://github.com/samuel/python-ping """
		sum = 0
		countTo = (len(source_string)/2)*2
		count = 0
		while count<countTo:
		    thisVal = ord(source_string[count + 1])*256 + ord(source_string[count])
		    sum = sum + thisVal
		    sum = sum & 0xffffffff
		    count = count + 2

		if countTo<len(source_string):
		    sum = sum + ord(source_string[len(source_string) - 1])
		    sum = sum & 0xffffffff

		sum = (sum >> 16)  +  (sum & 0xffff)
		sum = sum + (sum >> 16)
		answer = ~sum
		answer = answer & 0xffff
		answer = answer >> 8 | (answer << 8 & 0xff00)
		return answer

	async def ping_pong(self, ip):
		try:
		    ping_pack = struct.pack('!bbHHh', 8,0,0,1,1)
		    chk_summ = self.checksum(ping_pack.decode())
		    ping_pack = struct.pack('!bbHHh', 8,0,chk_summ,1,1)
		except Exception as exc:
			print('exc ping : ping_pong {}'.format(exc))

		try:
			with socket.socket(socket.AF_INET, socket.SOCK_RAW, socket.IPPROTO_ICMP) as s:
				s.sendto(ping_pack, (ip, 1))
				s.settimeout(self.timeout)
				
				recPacket, (addr, _) =  s.recvfrom(1024)
				(Type, Code, _, _, _)  = struct.unpack('!bbHHh', recPacket[20:28])
				s.settimeout(self.timeout)
				s.close()
				return {'Type' : Type, 'Code' : Code, 'Addr' :  addr, 'DateTime' : datetime.datetime.now().strftime('%d, %b %Y  %H:%M')}
		except Exception as exc:
			print('exc ping ping_pong {}'.format(exc))	

	async def ping_all(self):
		tasks = [self.ping_pong(ip) for ip in self.ip_list]
		done, _ = await asyncio.wait(tasks)	

		for item in done:
			try:
				# (Type,Code,addr, time) = item.result()
				# if( (Type == 0 ) and (Code == 0) ):
				if (item.result()['Type'] == 0) and (item.result()['Code'] == 0):
					# self.available_list.append((addr, time))
					self.available_list.append( { 'Addr' : item.result()['Addr'], 'DateTime' : item.result()['DateTime'] })
			except Exception as exc:
				print('exc ping ping_all {}'.format(exc))	

	def get_available_list(self):
		return self.available_list	

	def start(self):
		if sys.platform == "win32":
			self.loop = asyncio.ProactorEventLoop()
			asyncio.set_event_loop(self.loop)
		else:
			print('using not win32 arch. it demands the root priveleges!')
			self.loop = asyncio.new_event_loop()
			asyncio.set_event_loop(self.loop)			
			# self.loop = asyncio.get_event_loop()
		data = self.loop.run_until_complete(self.ping_all())
		self.loop.close()
		Available = self.get_available_list()
		length = len(Available)
		return {'Available' : Available, 'Length' : length}

def main():
	import json

	time0 = datetime.datetime.now()
	ip_range = range(1,25) 
	ip_address_list = [ '10.28.136.{}'.format(x) for x in ip_range] 
	P = Ping(ip_address_list, 0.04)
	dsting = json.dumps(P.start())
	lstring = json.loads(dsting)
	print(lstring)

	time1 = datetime.datetime.now() - time0
	print('exited with time {} \n'.format(time1))

if __name__ == '__main__':
	main()		