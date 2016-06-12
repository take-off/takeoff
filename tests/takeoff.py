class TakeOff(object):
  def __init__(connection_object, hostname, platform):
    self.connection = connection_object
    self.hostname = ''
    self.platform = ''
    self.status = False
    self.output = []
    self.error = []
    self.debug = []
  
class TakeOffError(Exception):
  pass
