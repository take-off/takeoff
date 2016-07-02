import sys
import socket
import yaml
import paramiko

TEST_DIR = 'tests'
TEST_LIST_FILE = 'test_list.yaml'


class TakeOffCore(object):

  def __init__(self, hostname,
                username=None, 
                password=None, 
                platform=None,
                test_dir=TEST_DIR,
                test_file=TEST_LIST_FILE,
                connection=None):
    self.hostname = hostname
    self.platform = platform
    self.username = username
    self.password = password
    self.test_dir = test_dir
    self.test_file = test_file
    self.test_list = self._get_test_list()

    # Calling code can create session outside of object
    # and pass it in, otherwise we'll ssh in here
    if connection:
      conn=connection
    if self.platform != 'fake':
      self.conn = self._get_device_connection()
    else:
      self.conn = None

  def _get_device_connection(self):
    conn = paramiko.SSHClient()
    conn.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    try:
      conn.connect(hostname=self.hostname,
                    username=self.username,
                    password=self.password)
    
    except paramiko.AuthenticationException:
      raise Exception("Authentication failed to device %s: %s" %
                      (hostname, e))
    except socket.ioerror as e:
      # would a custom exception work better here?
      raise Exception("Could not connect to device %s: %s" % 
                      (hostname, e))

    return conn

  """
  def _get_device_connection(self):
    conn = ConnectionManager.connection(
      target=self.hostname,
      user=self.username,
      password=self.password)

    if not conn.open():
      raise Exception("Could not log into %s, check connectivity and credentials." % self.hostname)

    return conn
  """

  def _get_test_list(self):
    test_list = []

    test_file_path = '%s/%s' % (self.test_dir, self.test_file)

    # Import list from json file
    try:
      with open(test_file_path) as f:
        y = yaml.load(f)
    except yaml.YAMLError as e:
      raise Exception("Could not parse YAML file %s: %s" % TEST_LIST_FILE, e)

    # Get common tests
    if y.get('common'):
      test_list.extend(y['common'])

    # Then platform
    if y.get(self.platform):
      test_list.extend(y[self.platform])

    return test_list

  def test_runner(self):
    state = True

    for testclass_name in self.test_list:
      if not self._run_test(testclass_name):
        state = False

    return state

  def _run_test(self, testclass_name):

    # testclass_name format is module.path.ClassName
    elements = testclass_name.split('.')
    # Classname is last element, rest is path
    classname = elements.pop()

    # First element
    testclass_path = elements.pop(0)

    # Then append anything else with dot notation
    for elem in elements:
      testclass_path += '.%s' % elem

    print "Running test: %s" % testclass_name

    # Now load and run test
    try:
      exec('from tests.%s import %s'% (testclass_path, classname))
    except ImportError as e:
      print "Could not import module %s: %s" % (testclass_name, e)

    exec('test_obj = %s.create(self)' % classname)

    # Then run the test, which will set self.status to true or false

    test_obj.test()

    if test_obj.status == True:
      print "---- TEST SUCCESS --- "
      for line in test_obj.output:
        print line
    else:
      print "---- TEST FAILED ----"
      for line in test_obj.output:
        print "  %s" % line
      for line in test_obj.error:
        print "  %s" % line
