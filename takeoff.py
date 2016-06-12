#!/usr/bin/env python2.7

import sys
import getpass
from optparse import OptionParser
from lib.takeoff_core import TakeOffCore

TEST_DIR = 'tests'
TEST_LIST_FILE = 'test_list.yaml'


def arg_parse(argstr):
  parser = OptionParser()
  parser.add_option('-u', '--username', help="Override username")
  parser.add_option('-t', '--testdir', help="Use alternate test directory")
  parser.add_option('-p', '--platform', help="Device platform")
  (options, args) = parser.parse_args(argstr)

  if not options.platform:
    print "Must specific platform type!"
    sys.exit(1)

  return options, args


def main():

  options, args = arg_parse(sys.argv[1:])

  if options.username:
    username = options.username
  else:
    username = getpass.getuser()

  if options.platform != 'fake':
    password = getpass.getpass("Enter device password: ")
  else:
    password = 'password'

  if options.testdir:
    test_dir = options.testdir
  else:
    test_dir = TEST_DIR

  test_file = TEST_LIST_FILE

  if not args[0]:
    print "Must specify filename"
    sys.exit(1)

  hostname = args[0]

  core = TakeOffCore(hostname=hostname,
                      username=username, password=password,
                      platform=options.platform, test_dir=test_dir,
                      test_file = test_file)

  core.test_runner()

if __name__ == '__main__':
  main()