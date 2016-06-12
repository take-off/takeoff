class TakeOff(object):
  def __init__(connection_object, hostname, platform):
    self.connection = connection_object
    self.hostname = ''
    self.platform = ''
    self.status = False
    self.output = []
    self.error = []
    self.debug = []

  def _handle_success(output):
    # Output can be single string or list of strings
    if not isinstance(output, list):
      output = [output]
    else:
      assert isinstance(output, str)

    self.output = output
    self.status = True
    return self.status

  def _handle_failure(output=[], error=[]):
    # Output can be single string or list of strings
    if not isinstance(output, list):
      output = [output]
    else:
      assert isinstance(output, str)

    # Error can be single string or list of strings
    if not isinstance(error, list):
      error = [error]
    else:
      assert isinstance(error, str)

    self.output = output
    self.error = error
    self.status = False
    return self.status
  
class TakeOffError(Exception):
  pass
