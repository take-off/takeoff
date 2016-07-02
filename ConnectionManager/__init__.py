#!/usr/bin/env python

import sys
import os
import re
import logging
import os, os.path
import paramiko
from time import sleep
from pprint import pprint
# ncclient
from ncclient import manager as netconf_ssh
import ncclient.transport.errors as NcErrors
import ncclient.operations.errors as NcOpErrors
from ncclient.operations import RPCError
# Arista pyeos
import pyeos

class Connection:
  def __init__(self,target=None,user=None,password=None,\
    key=None,timeout=30,debug=False):
    self.nc=None
    self.ssh=None
    self.target = target
    self.user = user
    self.password = password
    self.noop = False
    self.timeout = timeout
    self.private_key = key
    self.ssh = None # placeholder in case we want SSH
    self.debug = debug
    self.logger = self.__get_logger()
    self.__logger_handler = None
    self.__errors = list()
    self.__results = list()
    self.__netconf_port = 830
    self.__ssh_channel=None

  def __repr__(self):
    ssh_open = True if self.ssh else False
    nc_open = True if self.nc else False
    return "ControlMaster(<{}>, netconf={}, ssh={})".format(
            self.target,nc_open,ssh_open)

  def __get_logger(self):
   if not self.debug: return None
   logger = logging.getLogger('takeoff')
   # logging is split into a thread by python, so avoid duplicating
   # output if this module was called by another instance of __class__
   logger.setLevel(logging.DEBUG)
   if len(logger.handlers)>0:
     self.__logger_handler = logger.handlers[0]
   else:
     self.__logger_handler = logging.StreamHandler(sys.stderr)
     self.__logger_handler.setLevel(logging.DEBUG)
     formatter = logging.Formatter('%(asctime)s - '
                 + '%(levelname)-8s - ControlMaster.%(funcName)s: %(message)s')
     self.__logger_handler.setFormatter(formatter)
     logger.addHandler(self.__logger_handler)
   return logger

  def get_error(self):
    if self.debug: self.logger.debug("reporting error: {}".format(self.__e))
    #if self.__e is None: return False
    return self.__errors()

  def __exit(self):
    return dict(
      results = self.__results,
      errors = self.__errors
      )

  def cli(self,cmd):
    self.__errors = []
    self.__results = []

    if self.debug: self.logger.debug("cli({})".format(type(cmd)))
    if self.ssh is None:
      try:
        self.__ssh_connect()
      except:
        self.__errors.append("Unable to open SSH session")
        return self.__exit()
      #
      # send command
      #
    if type(cmd) is str:
      self.__cli_cmd(cmd)
    elif type(cmd) is list:
      self.__cli_cmd_list(cmd)

    # return results
    return self.__exit()

  def __cli_cmd(self, cmd):
    if self.debug: self.logger.debug("{}".format(cmd))
    try:
      stdin,stdout,stderr = self.ssh.exec_command("{}".format(cmd))
      self.__results.append(stdout.read())
    except:
      self.__errors.append("Command failed: {}".format(cmd))
      return False
    return True

  def __cli_cmd_list(self, cmd_list):
    if self.debug:
      self.logger.info("Running list of commands")
    for cmd in cmd_list:
      self.__cli_cmd(cmd)

  def cli_batch(self, cmds):
    self.__errors = list()
    self.__results = list()

  if self.debug:
    self.logger.info("Invoking shell for multiple commands")
  try:
    chan = self.ssh.invoke_shell()
  except:
    self.__errors.append("SSH channel initialization failed")
    return self.__exit()
  try:
    chan.send("{}\n".format(cmds))
    while not chan.recv_ready():
      sleep(5)
      self.__results.append(chan.recv(99999))
  except Exception as e:
    self.__errors.append("Command set failed")
    return self.__exit()
  return self.__exit()


  # ------------------------------------------------------------------------
  # handle netconf connections
  # ------------------------------------------------------------------------
  def __nc_connect(self):
    if self.debug:
      self.logger.info("netconf connecting to {}".format(self.target))

    if self.target is None or self.user is None: return False
    try:
      if self.private_key is not None:
        pass # handle keys later
      else:
        self.nc = netconf_ssh.connect(
                  host=self.target,
                  port=self.__netconf_port,
                  username=self.user,
                  password=self.password,
                  )
    except Exception as e:
      self.__errors = "Unknown error occurred"
      return False

    if self.debug:
      self.logger.info("connected to {}".format(self.target))

    # set custom timeout for connection
    # self.nc.timeout = self.timeout
    return True

  def __nc_close(self):
    if self.debug:
      self.logger.debug("closing netconf session: {}".format(self.target))
    if self.nc is None: return False
    try:
      self.nc.close()
      self.nc=None
    except:
      self.__errors.append("Error closing connection")
      return False
    return True

  def open(self,netconf=False,ssh=True):
    # attempt to open both netconf and ssh..
    nc_open=False
    ssh_open=False
    if netconf and self.nc is None:
      nc_open = self.__nc_connect()
    if ssh and self.ssh is None:
      ssh_open = self.__ssh_connect()
    if not (ssh_open or nc_open):
      return False
    return True

  def rpc(self, xmlrpc):
    self.__errors = list()
    self.__results = list()

    if self.nc is None: self.open()
    if type(xmlrpc) is str:
      self.__rpc(xmlrpc)
    elif type(xmlrpc) is list:
      for cmd in xmlrpc:
        self.__rpc(cmd)
    return self.__exit()

  def __rpc(self, xmlrpc):
    try:
      self.nc.rpc("{}".format(xmlrpc))
    except Exception as e:
      self.__errors.append("An RPC error occurred: {}".format(e))
        return False
    return True


  # ------------------------------------------------------------------------
  # handle ssh connections
  # ------------------------------------------------------------------------
  def __ssh_connect(self):
    """
    Connect to device using SSH/paramiko
    """
    if self.debug:
      self.logger.info("ssh connecting to {}".format(self.target))

    if self.ssh is None:
      self.ssh = paramiko.SSHClient()
    self.ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())

    try:
      if self.private_key is not None and os.path.isfile(self.private_key):
        self.ssh.connect(self.target, username=self.user, \
                      pkey=self.private_key, timeout=self.timeout)
      else:
        self.ssh.connect(self.target, username=self.user, \
                      password=self.password, timeout=self.timeout)

    except:
      self.__errors.append("Unable to SSH to {}".format(self.target))
      return False

    return True

  #----------------------------------------------------------------------
  # Close out connections
  #----------------------------------------------------------------------
  def __ssh_close(self ):
    if self.ssh: self.ssh.close()

  #----------------------------------------------------------------------
  # Close out connections
  #----------------------------------------------------------------------
  def close(self):
    if self.nc: self.__nc_close()
    if self.ssh: self.__ssh_close()



##class JnprController
################################################################################
