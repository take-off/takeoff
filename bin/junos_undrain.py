from takeoff import ConnectionManager
from getpass import getpass,getuser


junos = { 'isis': 'delete protocols isis overload',
	  'ospf': 'delete protocols ospf overload',
          'bgp': 'activate protocols bgp'
        }

def genconf(protocol):
	junos_string="""configure
	      		{}
	      		show | compare
	      		commit and-quit""".format(junos[protocol])
	return junos_string

def exec(cmd):
    res = conn.cli_batch(cmd)
    if 'error' in res:
        print '{} Commands not executed on {}'.format(cmd,target)
    else:
         for result in res['results']:
	    parse_result(result)

if __name__ = '__main__':
    username = getuser()
    password = getpass('Your Password: ')
    device = raw_input('Target device: ')

    conn = ConnectionManager.connection(
        target=device,
        user=username,
        password=password
        )
    isis_str = genconf('isis')

    if conn.open():
	exec(isis_str)
    else:
	print "Connection not established to {}".format(device)

