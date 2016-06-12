class TakeOffTest(object):
  def __init__(self, connection_object, hostname, platform):
    self.connection = connection_object
    self.hostname = ''
    self.platform = ''
    self.status = False
    self.output = []
    self.error = []
    self.debug = []

  @classmethod
  def factory(cls, connection_object, hostname, platform):
    obj = cls(connection_object=connection_object,
                hostname=hostname, platform=platform)
    obj.output = []
    obj.error = []
    obj.debug = []
    return obj

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
