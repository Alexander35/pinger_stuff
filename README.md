# pinger_stuff

# ping all 10.28.x.x example


	time0 = datetime.datetime.now()
	ip_range = range(0,20) 
	ip_address_list = [ '10.28.{}.{}'.format(x, y) for x in ip_range for y in ip_range] 
	P = pinger_stuff.Ping(ip_address_list, 0.04)
	(available, length) = P.start()
	print('availbale hosts {} \n len {}'.format(available , length))

	time1 = datetime.datetime.now() - time0
	print('exited with time {} \n'.format(time1))