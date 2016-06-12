from takeoff_test import TakeOffTest


class InterfaceTest(TakeOffTest):

  def __init__(self, connection_object, hostname, platform):

    super(InterfaceTest, self).__init__(connection_object=connection_object,
                                           hostname=hostname,
                                          platform=platform)

  def test(self):

    res = connection_object.cli('show inter description')
  def pasre_interfaces(cmd_out, platform):
    interfaceline = cmd_out
    platform =  platform
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
