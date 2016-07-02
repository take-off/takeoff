from ..takeoff_test import TakeOffTest
import re

class AristaBGPConnTest(TakeOffTest):

  def test(self):

    neighbor_line_re = re.compile('(^\s*\d+\.\d+\.\d+\.\d+).*')

    stdin, stdout, stderr = self.conn.exec_command('show ip bgp summary')

    neighbor_lines = []
    #for line in res['results'][0].split('\n'):
    for line in stdout.readlines():
      line.rstrip('\n')
      if neighbor_line_re.match(line):
        neighbor_lines.append(line)

    for neighbor in neighbor_lines:
      neighbor_line_split = neighbor.split()
      #print "DEBUG: %s" % neighbor_line_split
      neighbor_ip = neighbor_line_split[0]
      neighbor_state = neighbor_line_split[-1]
      # Then test the neighbor
      self.nei_fun(neighbor_ip, neighbor_state)

    if len(self.error) == 0:
      self._handle_success()
    else:
      self._handle_failure()

  def nei_fun(self, nei_addr, nei_state):
    #print nei, nei_name
    #print type(nei), type(nei_name)
    #print "DEBUG: %s %s" % (nei_addr, nei_state)

    if nei_state.isdigit():
      self.output.append("Peer %s is up, %s prefixes" % (nei_addr, nei_state))
    else:
      self.error.append('Peer %s not up, in state %s' % (nei_addr, nei_state))

    # except ValueError as e:
    # print "BGP peering with", nei_name, "is Down"

    # for neighbor in range(iteration):
    #  nei=pfile_l[index_version+10*neighbor]
    #  temp=index_version+10*neighbor
    #  nei_name=pfile_l[temp+1]
    #  #print nei, temp, nei_name
    #  #print type(nei), type(temp), type(nei_name)
    #  nei_fun(nei, nei_name)
