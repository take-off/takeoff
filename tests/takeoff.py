class TakeOff(object):
  def __init__(connection_object):
    self.connection = connection_object
    self.status = False
    self.output = []
    self.error = []
    self.debug = []

class TakeOffError(Exception):
  pass
