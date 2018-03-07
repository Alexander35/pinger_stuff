# pinger_stuff

## ping 10.38.139.x example:

P.start() return something like this :

```{'Available': [{'Addr': '10.38.139.18', 'DateTime': '07, Mar 2018  10:45'}, {'Addr': '10.38.139.21',
 'DateTime': '07, Mar 2018  10:45'}, {'Addr': '10.38.139.11', 'DateTime': '07, Mar 2018  10:45'}, {'
Addr': '10.38.139.23', 'DateTime': '07, Mar 2018  10:45'}, {'Addr': '10.38.139.12', 'DateTime': '07,
 Mar 2018  10:45'}, {'Addr': '10.38.139.16', 'DateTime': '07, Mar 2018  10:45'}, {'Addr': '10.38.139
.14', 'DateTime': '07, Mar 2018  10:45'}], 'Length': 7}```

so, you can convert it to JSON

	time0 = datetime.datetime.now()
	ip_range = range(1,25) 
	ip_address_list = [ '10.28.136.{}'.format(x) for x in ip_range] 
	P = Ping(ip_address_list, 0.04)
	dsting = json.dumps(P.start())
	lstring = json.loads(dsting)
	print(lstring['Available'][5]['Addr'])
	print(lstring['Available'][5]['DateTime'])

	time1 = datetime.datetime.now() - time0
	print('exited with time {} \n'.format(time1))