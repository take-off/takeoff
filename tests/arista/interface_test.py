import re
from ..takeoff_test import TakeOffTest

INT_REGEX = re.compile('^Et.+')

class InterfaceTest(TakeOffTest):

  def test(self):

    stdin, stdout, stderr = self.conn.exec_command('show interface status')
    self._parse_interfaces(stdout)
  
  def _parse_interfaces(self, cmd_out):
    platform = self.platform
    down = list()
    up = list()      
    interfacelines = cmd_out.readlines()
    for i in interfacelines:
      i.rstrip('\n')
      if INT_REGEX.match(i):
        if ('admin down' in i) or ('down' in i):
          downinterface = i.split()[0]
          down.append(downinterface)
        if ('up' in i) or ('connected' in i):
          upinterface = i.split()[0]
          up.append(upinterface) 
    # Then test the interfaces
    self.interface_fun(down, up)

    if len(self.error) == 0:
      self._handle_success()
    else:
      self._handle_failure()

  def interface_fun(self, down, up):
    if len(down) != 0:
      self.error.append(" %s interface are DOWN, DOWN interfaces:" % (len(down)))
      for interface in down:
        self.error.append("  %s" % interface)
    else:
      self.output.append(" %s interfaces are UP, UP interfaces:" % (len(up)))
      for interface in up:
        self.output.append("  %s" % interface)
