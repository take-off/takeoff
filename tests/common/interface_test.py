from ..takeoff_test import TakeOffTest


class InterfaceTest(TakeOffTest):

  def test(self):

    res = connection_object.cli('show interface description')
    self.parse_interfaces(res)
  
  def parse_interfaces(self, cmd_out):
    interfaceline = cmd_out
    platform = self.platform
    down = list()
    up = list()      
    interfaceline = cmd_out.splitlines()
    for i in interfaceline:
        if 'admin down' in i  or 'down' in i:
            downinterface = i.split()[0]
            down.append(downinterface)
        if 'up' in i:
            upinterface = i.split()[0]
            up.append(upinterface) 
    # Then test the interfaces
    self.interface_fun(down, up)

    if len(self.error) == 0:
      self._handle_success()


  def interface_fun(down, up):
    if down is not None:
      self.output.append(" %s interface are DOWN, %s DOWN interfaes" % (len(down), down))
    else:
      self.error.append(' %s interfaces are UP, UP interfaces %s' % (len(up), up))
