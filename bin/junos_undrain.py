import ConnectionManager


conn = ConnectionManager.connection(
        target=myhostname,
        user=user,
        password=password
        )

junos = { 'isis': 'delete protocols isis overload',
	  'ospf': 'delete protocols ospf overload',
          'bgp': 'activate protocols bgp'
        }

def genconf(protocol):
	junos_string="""configure
	      		{}
	      		show | compare
	      		commit and-quit""".format(protocol)
	return junos_string

def exec(cmd):

    if conn.open():
       	res = conn.cli_batch(cmd)
       	if 'error' in res:
             print '{} Commands not executed on {}'.format(cmd,target)
	else:
            for result in res['results']:
	        parse_result(result)
    else:
	print "Connection not established to {}'.format(target)

if __name__ = '__main__':

