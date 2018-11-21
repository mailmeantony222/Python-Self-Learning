###############################################################################################################
import datetime
import subprocess
import shlex
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
        print "Usage: python BMC_HPM_Fw_Upgarde_Loop_test.py"
        exit()

import os, time, json, StringIO

yes_no_prompt = "yes/no"
yes_no_prompt1 = "(Please enter 'yes' or 'no')"
pswd_prompt = "password:"
sys_prompt1 = ("\$")
sys_prompt2 = ("]\#")
sys_prompt3 = (".*#")


#Give BMC IP of the Board
bmcip = "10.7.13.228" #(User should update)

#ipmi username, password
ipmi_username = "admin"
ipmi_password = "admin"

#Give IP,user_name,password of remote machine from where you want to run the test
#(User should update, host ip means the ip address of machine from where user wants to run the script)
hostip = "10.7.16.98" 
host_username = "root"
host_password = "caveo123"

#Give the board OS type
board_os_type = "centos"#(User should update)

#Give Telnet ip, port_nu of the board
#User should update below fields
telnet_ip = "10.7.15.11"
telnet_port = "7016"

#Give the path of the file to store sensor output
#User should give the path of file to store the sensor o/p.
sensor_file = open(os.path.join("/","home","Sensor_logs.txt"),"a")

#Give the path of the file to store logs
#User should give the path of the file to store the logs.
log_file = open(os.path.join("/","home","Test_logs.txt"),"a")

#Give the number of iteration
limit = 300

#Give system password
#User should give the linux password
sys_password="centos"

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

def ipmiPowerCycle(bmcip, host_ip, host_username="root", host_password="caveo123", ipmi_username="admin", ipmi_password="admin"):
    '''
        Used to power cycle the board using ipmitool command.
    [Args]
        bmcip - [str] IP address of BMC.
        host_ip - [str] System IP in which the commands needs to be executed.
        host_username - [str] System username in which the commands need to be executed.
        host_password - [str] System password in which the commands need to be executed.
        ipmi_username - [str][optional] BMC IPMI username. 
        ipmi_password - [str][optional] BMC IPMI password.
    [Return]
        Returns execution logs in case of seccess.
        Returns Exception in case of failure.
    '''
    try:
        sshlog = StringIO.StringIO()
        sshfun = ssh(host=host_ip, username=host_username, password=host_password , logname=sshlog)
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

def ipmioverlanplus(ip, sysip, command, sys_username="root", sys_password="caveo123", username="admin", password="admin"):
    ''' This function is used to run command over lanplus environment
    Args
        ip - [String] BMC IP.
        command - [String] Command to run to BMC over lanplus environment.
        username - [string][optional] Username of BMC.
        password - [string][optional] Password of BMC.
    Returns
        Logs - Execution console logs.
        Taken Time - time taken during execution.
    '''
    try:
        starttime = time.time()
        #sshlog = StringIO.StringIO()
        #sshfun = ssh(host=sysip, username=sys_username, password=sys_password , logname=sshlog)
        cmdstring = "ipmitool -H " + str(ip) + " " + str(command) + " -U " + str(username) + " -P " + str(password) + " -I lanplus"
        log = "\nCommand: "+ str(cmdstring) +"\nOutput:\n=======\n"
        #sshfun.send(cmdstring)
    #(prompt, log) = sshfun.expect([".*#"], timeout = 60, enableLogs=True)
    #print log
    #log = log.replace("[root@localhost ~]#","")
    #log = log.replace("root@localhost ~","")
        log += subprocess.check_output(shlex.split(cmdstring), stderr=subprocess.STDOUT)
        endtime = time.time()
        takentime = "{0:.2f}".format(endtime-starttime)
        #sshfun.close()
        return log, float(takentime)
    except subprocess.CalledProcessError as e:
        print "Ipmitool lanplus failed with errorcode: "+str(e.returncode)+" \nOUTPUT:\n========\n"+str(e.output)
        #sshfun.close()
        raise Exception ("Ipmitool lanplus failed with errorcode: "+str(e.returncode)+" \nOUTPUT:\n========\n"+str(e.output))

def setup(num_of_itr):
    global telnetfun
    global telnetlog
    tclogs = ''
    try:

        (res, log) = telnetfun.expect('Switching console to secure uart', enableLogs=True, timeout=100)
        tclogs += str(log)
        time.sleep(10)
        out, time1 = ipmioverlanplus(bmcip, sysip=hostip, command="sdr type temperature" , username=ipmi_username, password=ipmi_password)
        tclogs += out
        print str(out)
        sensor_file.write("\n=============================================Iteration %s===============================================\n"%(str(num_of_itr))+str(out))

        if board_os_type == "ubuntu":
            (res, log) = telnetfun.expect('ubuntu login:', enableLogs=True, timeout=900)
            tclogs += str(log)

        elif board_os_type == "centos" or board_os_type == "rhel":
            (res, log) = telnetfun.expect('localhost login:', enableLogs=True, timeout=900)
            tclogs += str(log)

        telnetfun.send(host_username)
        (res, log) = telnetfun.expect('Password:', enableLogs=True, timeout=120)
        telnetfun.send(sys_password)
        (res, log) = telnetfun.expect([']\#',pexpect.TIMEOUT], enableLogs=True, timeout=120)
        tclogs += str(log)
        tclogs+=("\n\n\n##########################  Rebooting the system #########################\n\n\n")
        print "\n################################ Rebooting the System ###########################\n"
        telnetfun.send("reboot")
        (res, log) = telnetfun.expect('Rom...', enableLogs=True, timeout=120)
        tclogs += str(log)
        return (tclogs,"p")

    except pexpect.TIMEOUT:
        print "\n\n###### Timeout Exception, Server may not responding ######\n\n"
        tclogs += "\n\n###### Timeout Exception, Server may not responding ######\n\n"
        return (tclogs,"f")

    except Exception as e:
        print "\nException in test\n" + str(e)
        tclogs += "\nException in test\n"+str(e)
        return (tclogs,"f")

def FTC1():
    starttime = time.time()
    global telnetlog, telnetfun, limit
    logs = ""
    try:
         telnetlog = StringIO.StringIO()
         telnetfun = telnet(host=telnet_ip, port=telnet_port,logname=telnetlog)
         log = ipmiPowerCycle(bmcip, hostip)
         for itr in range(limit):
             logs += "\n\n\n##########################  TEST ITERATION: %s #########################\n\n\n"%str(itr)
             print "\n###################################### TEST ITERATION : %s ##########################\n"%str(itr)
             log, res = setup(itr)
             logs += str(log)
             log_file.write(logs)
             if res == "f":raise Exception("Exiting from script due to exception")
             logs = ""

    except Exception as e:
         print "\nException found\n" +str(e)
    endtime = time.time()
    takentime = "{0:.2f}".format(endtime - starttime)
    telnetfun.close()


if __name__ == '__main__':
   FTC1()
