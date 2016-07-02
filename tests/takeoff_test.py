class TakeOffTest(object):
  def __init__(self, core):
    self.core = core
    # Copy data from core into attributes for easier reference
    self.conn = core.conn
    self.hostname = core.hostname
    self.platform = core.platform
    self.status = False
    self.output = []
    self.error = []
    self.debug = []

  @classmethod
  def create(cls, core):
    obj = cls(core)
    obj.state = None
    obj.output = []
    obj.error = []
    obj.debug = []
    return obj

  def get_state(self):
    return self.state

  def set_state(self, state):
    self.state = state

  def _handle_success(self, output=[]):
    # Output can be single string or list of strings
    if isinstance(output, str):
      output = [output]
    else:
      assert isinstance(output, list)

    self.output.extend(output)
    self.status = True
    return self.status

  def _handle_failure(self, output=[], error=[]):
    # Output can be single string or list of strings
    if isinstance(output, str):
      output = [output]
    else:
      assert isinstance(output, list)

    # Error can be single string or list of strings
    if isinstance(error, str):
      self.error = [error]
    else:
      assert isinstance(error, list)

    self.output.extend(output)
    self.error.extend(error)
    self.status = False
    return self.status

class TakeOffError(Exception):
  pass
