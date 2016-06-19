from ..takeoff_test import TakeOffTest

class SuccessTest(TakeOffTest):

  """
  Elements of Superclass will be:
  self.status = defaults to False. Set to True before returning method.
  self.output = standard status output that we expect test running to emit.
                return multiple lines as list.
  self.error = If error, send
  self.debug = list() element. If desired, output verbose output by
              appending text lines to this attribute.

  Calling code will initiate the object, passing in a connection
  object, the hostname, and platform string.
  It will then call the object's test() method (which takes no args).

  test() method is expected to set self.status to True or False, and return
  the same value.
  """
  def test(self):

    # Run arbitrary tests here #
    self.debug.append("Running this test")

    # Test successful! Call the appropriate method with optional
    # additional output. Output arg can be one string or list
    # of strings.
    return self._handle_success(output="Found X interfaces, all up!")

class FailureTest(TakeOffTest):

  def test(self):

    self.debug.append("Running this test")
    return self._handle_failure(
              output="Found X interfaces up",
              error=["Found interface X down", "Found interface Y down"])
