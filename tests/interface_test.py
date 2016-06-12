#Test case for Interface UP/down

cmd_out = """R1#sho interfaces description
Interface                      Status         Protocol Description
Fa0/0                          up             up
Fa0/1                          down     down
Se1/0                          admin down     down
Se1/1                          up             up
Se1/2                          admin down     down
Se1/3                          admin down     down"""


platform = 'cisco'

class interfaceTest:
    def __init__(self,cmd_out, platform):
        self.interfaceline = cmd_out
        self.platform =  platform
        self.down = list()
        self.up = list()
    def pasre_interfaces(self, cmd_out, platform):
        self.interfaceline = cmd_out.splitlines()
        for i in self.interfaceline:
            if 'admin down' in i  or 'down' in i:
                downinterface = i.split()[0]
                self.down.append(downinterface)
            if 'up' in i:
                upinterface = i.split()[0]
                self.up.append(upinterface)
        return len(self.down) , self.down, len(self.up), self.up
test=  interfaceTest(cmd_out,platform)
print test.parse_interfaces(cmd_out,platform)
