""" It works slowly. it uses a ping comand from os / Disigned for Microsoft Windows 7"""

import asyncio
import os
import sys
import re
import datetime 

class PingProtocol(asyncio.SubprocessProtocol):
    def __init__(self, exit_future):
        self.exit_future = exit_future
        self.output = bytearray()

    def pipe_data_received(self, fd, data):
        self.output.extend(data)

    def process_exited(self):
        self.exit_future.set_result(True)

class PingerStuff:
	"""this is for simple monitoring PingerStuff"""
	def __init__(self, ip_list, n=2, l=16384, w=500):
		self.ip_list = ip_list
		self.n = n
		self.l = l
		self.w = w
		self.list = []

	def get_list(self):
		return self.list	

	def print_list(self):
		[print('{} \n'.format(self.list[i])) for i in range(len(self.list)) if self.list != []]	

	async def get_status(self, data):
		try:
			avg = re.search(r'(?<=Average = )\w+', data)
			ip_address = re.search(r'Pinging (.*?)with', data).group(1)

			if((avg != None)):
				if(avg.group(0)):
					self.list.append({ip_address : avg.group(0) , 'time' : datetime.datetime.now()})
		except Exception as exc:
			pass

	async def ping_one(self, ip):
		exit_future = asyncio.Future(loop=self.loop)
		create = self.loop.subprocess_shell(
		    	lambda: PingProtocol(exit_future),
				'ping {} -n {} -l {} -w {} -a'.format(ip, self.n, self.l, self.w),
				stdin=None, stderr=None
			)
		transport, protocol = await create
		await exit_future
		transport.close()
		data = bytes(protocol.output)
		return await self.get_status(data.decode('cp1251'))

	async def ping_all(self):
		tasks = [self.ping_one(ip) for ip in self.ip_list]
		done , _ = await asyncio.wait(tasks)

	def ping(self):
		if sys.platform == "win32":
			self.loop = asyncio.ProactorEventLoop()
			asyncio.set_event_loop(self.loop)
		else:
			self.loop = asyncio.get_event_loop()
		data = self.loop.run_until_complete(self.ping_all())
		self.loop.close()

def main():
	time0 = datetime.datetime.now()
	ip_range = range(1,254) 
	ip_address_list = [ '10.28.{}.{}'.format(x,y) for x in ip_range for y in ip_range] 
	os.system('chcp 437')
	for i in range(0,600):
		PS = PingerStuff(ip_address_list[i*100:i*100+100], 4, 32, 500)
		PS.ping()
		PS.print_list()

	time1 = datetime.datetime.now() - time0
	print('exited with time {} \n'.format(time1))

if __name__ == '__main__':
	main()