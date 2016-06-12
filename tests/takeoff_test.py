class TakeOffTest(object):
  def __init__(self, connection_object, hostname, platform):
    self.connection = connection_object
    self.hostname = ''
    self.platform = ''
    self.status = False
    self.output = []
    self.error = []
    self.debug = []

  def _handle_success(self, output):
    # Output can be single string or list of strings
    if isinstance(output, str):
      output = [output]
    else:
      assert isinstance(output, list)

    self.output = output
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
      error = [error]
    else:
      assert isinstance(error, list)

    self.output = output
    self.error = error
    self.status = False
    return self.status

class TakeOffError(Exception):
  pass
