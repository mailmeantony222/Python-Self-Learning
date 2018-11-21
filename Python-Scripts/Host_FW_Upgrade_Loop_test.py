###############################################################################################################
import datetime
import sys
import re
import os
import select
import time
import pexpect
import json
import string
import random
from collections import OrderedDict
import fileinput
import glob
import pyExcelerator
import telnetlib
import pdb

if len(sys.argv) > 1:
        print "Usage: python Host_FW_Upgrade_Loop_test.py"
        exit()

import os, time, json, StringIO

yes_no_prompt = "yes/no"
yes_no_prompt1 = "(Please enter 'yes' or 'no')"
pswd_prompt = "password:"
sys_prompt1 = ("\$")
sys_prompt2 = ("]\#")
sys_prompt3 = (".*#")


#Give BMC IP of the Board
bmcip = "10.7.13.229"

#ipmi username, password
ipmi_username = "admin"
ipmi_password = "admin"

#Give IP,user_name,password of remote machine from where you want to run the test
hostip = "10.7.16.98"
host_username = "root"
host_password = "caveo123"

#Give Telnet ip, port_nu of the board
telnet_ip = "10.7.15.11"
telnet_port = "7015"

#Give Linux access details
username = "root"
password = "centos"

#Give the path of Host FW image on the host
fwpath = "/home/milinkm/Saber-BMC-Utils/7.1/bmc.hpm"

#Give the path of the file to store the logs
log_file = open(os.path.join("/","home","Host_FW_update_logs.txt"),"a")


class ProgramConnection:
    "Connection via PExpect to any interactive program (telnet, , ftp)."

    def __init__(self, command=None, logfile="test.log"):
        self.logname = logfile
        self.logging = Log(logfile)
        if command:
            self.connect(command)

    def connect(self, command, timeout):
        self.logging.logInfo("pexpect: spawning command '" + command + "'")
        self.conn = pexpect.spawn(command,timeout=timeout)
        self.conn.logfile = sys.stdout
        self.conn.delaybeforesend = 0.5

    def close(self):
        self.logging.logInfo("pexpect: closing connection")
        self.logging.close()
        try:
            self.conn.close(force=True)
        except pexpect.ExceptionPexpect:
            try:
                self.conn.close(force=True)
            except pexpect.ExceptionPexpect:
                pass
    def send_crt(self, data):
        self.logging.logInput(data)
        self.conn.sendcontrol(str(data))

    def log(self, data):
        self.logging.logInfo(data)

    def send(self,str):
        self.logging.logInfo(str)
        self.conn.sendline(str)

    def expect(self,pattern, enableLogs=False, timeout=60):
       ret = self.conn.expect(pattern, timeout=timeout)
       if type(self.conn.before) is str:
           self.logging.logOutput(self.conn.before + "\n")
       if type(self.conn.after) is str:
           self.logging.logOutput(self.conn.after + "\n")
       if enableLogs: return(ret, str(self.conn.before)+str(self.conn.after))
       return ret

def ipmiPowerCycle(bmcip, sysip, sys_username="root", sys_password="caveo123", ipmi_username="admin", ipmi_password="admin"):
    '''
        Used to power cycle the board using ipmitool command.
    [Args]
        bmcip - [str] IP address of BMC.
        sysip - [str] System IP in which the commands needs to be executed.
        sys_username - [str] System username in which the commands need to be executed.
        sys_password - [str] System password in which the commands need to be executed.
        ipmi_username - [str][optional] BMC IPMI username. 
        ipmi_password - [str][optional] BMC IPMI password.
    [Return]
        Returns execution logs in case of seccess.
        Returns Exception in case of failure.
    '''
    try:
        sshlog = StringIO.StringIO()
        sshfun = ssh(host=sysip, username=sys_username, password=sys_password , logname=sshlog)
        sshfun.send("ipmitool -I lanplus -H "+bmcip+" -U "+ipmi_username+" -P "+ipmi_password+" chassis power status")
        res, beforelog = sshfun.expect([".*#"], enableLogs=True, timeout=60)
        if 'Chassis Power is off' in beforelog:
            sshfun.send("ipmitool -I lanplus -H "+bmcip+" -U "+ipmi_username+" -P "+ipmi_password+" chassis power on")
        else:
            sshfun.send("ipmitool -I lanplus -H "+bmcip+" -U "+ipmi_username+" -P "+ipmi_password+" chassis power cycle")
        res, beforelog = sshfun.expect([".*#"], enableLogs=True, timeout=60)
        a = str(sshlog.getvalue())
        sshfun.close()
        sshlog.close()
        if res == 0: return a
        else: raise Exception("Failed to power cycle the board")
    except Exception as e:
        print str(e)
        print sshlog.getvalue()
        sshfun.close()
        sshlog.close()
        raise Exception(e)

class Log:
    def __init__(self, filename):
        self.file = filename 
        self.outputbuf = ""

    def close(self):
        self.flush()
        self.file.close()

    def flush(self):
        if self.outputbuf:
            for l in self.outputbuf[0:-1].split("\n"):
                self.file.write(">>> " + l + "\n")
            self.outputbuf = ""
        self.file.flush();

    def _write(self, data):
        self.flush()
        self.file.write("["+datetime.datetime.now().strftime("%H:%M:%S.%f")+"]"+data)


    def logOutput(self, data):
        self.outputbuf += data
        if data == "\n":
            self.flush()

    def logInfo(self, data):
        self._write("*** " + data + "\n")



class telnet(ProgramConnection):
    "Connection to a telnet device port"
    def __init__(self, host="127.0.0.1", port="root", logname="test.log"):
           ProgramConnection.__init__(self, None, logname)
           self.connect("timeout 360000 telnet %s %s" %(host,port), timeout=60)
           prompt = self.conn.expect(["Connected to.*","<CTRL>Z"], timeout = 60)
           if prompt == 0:
               self.success = 1
               return


class ssh(ProgramConnection):
    "Connection to a ethernet device"
    def __init__(self, host="127.0.0.1", username="root", password="root", logname="test.log"):
        ProgramConnection.__init__(self, None, logname)
        self.connect("ssh %s@%s" %(username,host), timeout=60)
        self.success = 1
        prompt = self.conn.expect([yes_no_prompt, pswd_prompt, sys_prompt1, sys_prompt2, sys_prompt3, "IDENTIFICATION", pexpect.TIMEOUT, pexpect.EOF], timeout = 60)
        if prompt == 4:
            os.system("ssh-keygen -f ~/.ssh/known_hosts  -R %s"%(host))
            self.connect("ssh %s@%s" %(username,host), timeout=60)
            prompt = self.conn.expect([yes_no_prompt, pswd_prompt, sys_prompt1, sys_prompt2 , sys_prompt3, pexpect.TIMEOUT, pexpect.EOF], timeout = 60)
        if prompt == 0:
                self.send("yes")
                time.sleep(1)
                prompt = self.conn.expect([yes_no_prompt, pswd_prompt, sys_prompt1, sys_prompt2, sys_prompt3, pexpect.TIMEOUT, pexpect.EOF], timeout = 60)
        if prompt == 1:
                self.send(password)
        if prompt > 3:
                self.success = 0
                return
        self.expect([sys_prompt1, sys_prompt2, sys_prompt3])
    

def FTC1():
    starttime = time.time()
    i,temp = 0,0
    log = ""
    try:
       #telnetlog = StringIO.StringIO()
       #telnetfun = telnet(host=telnet_ip, port=telnet_port, logname=telnetlog)

       sshlog = StringIO.StringIO()
       sshfun = ssh(host=hostip, username=host_username, password=host_password , logname=sshlog)
       
       
       while i < 200:
          sshfun.send("ipmitool -H "+str(bmcip)+" -I lanplus -U "+str(ipmi_username)+" -P "+str(ipmi_password)+" hpm upgrade "+str(fwpath)+" -z 0x7fff component 2 force ")
          (prompt, tlog) = sshfun.expect([".*"], timeout = 30, enableLogs=True)
          sshfun.send("y")
          log += str(tlog)
          (prompt, tlog) = sshfun.expect(["Firmware upgrade procedure successful", "Firmware upgrade procedure failed"], timeout = 300, enableLogs=True)
          log += str(tlog)
          if prompt == 1: raise Exception("Failed to update firmware on board")
          sshfun.send("ipmitool -H "+str(bmcip)+" -I lanplus -U "+str(ipmi_username)+" -P "+str(ipmi_password)+" sol activate  ")
          print ipmiPowerCycle(bmcip, hostip)
          (a,b)=sshfun.expect(["localhost login","ubuntu login:", pexpect.TIMEOUT],enableLogs=True, timeout=1500)
          log += str(b)
          if a == 2: raise Exception(str(b)+"\nObserved timeout, marking test case as fail")
          sshfun.send(username)
          (a,b)=sshfun.expect(["Password:"],enableLogs=True, timeout=1500)
          log += str(b)
          sshfun.send(password)
          (a,b)=sshfun.expect(["]\#"],enableLogs=True, timeout=1500)
          log += str(b)
          sshfun.send("ipmitool sensor")
          (a,b)=sshfun.expect(["]\#"],enableLogs=True, timeout=1500)
          log += str(b)

          if "Unable to establish IPMI" in str(b):
             tc.tcresult = "f"
             raise Exception("unable to send command in %s iteration"%str(i))

          print "==============================================================Count = %s ==============================================================="%str(i)
          log += "\n=====================================================Count = %s ======================================================="%str(i)
          log_file.write(log)
          log = ""
          i += 1
          sshfun.send("ipmitool -H "+str(bmcip)+" -I lanplus -U "+str(ipmi_username)+" -P "+str(ipmi_password)+" sol deactivate  ")
          (prompt, tlog) = sshfun.expect([".*#"], timeout = 60, enableLogs=True)
    except Exception as e:
       print e
       print "Test failed at %s iteration "%(str(i))
       log += str(e)
       log_file.write(log)
    sshlog.close()
    sshfun.close()

    endtime = time.time()
    takentime = "{0:.2f}".format(endtime - starttime)



if __name__ == '__main__':
   FTC1()

