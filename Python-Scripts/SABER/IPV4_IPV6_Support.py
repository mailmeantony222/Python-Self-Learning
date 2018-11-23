#!/usr/bin/python
# -*- coding: utf-8 -*-


import time
import os
import sys
import fileinput

import requests

class color:
      GREEN='\033[92m'
      RED='\033[91m'
      END='\033[0m'
      PURPLE='\033[35m'
      YELLOW='\033[93m'
      CYAN='\033[36m'
      PINK='\033[95m'
      BLUE='\033[44m'  





IPv4eth1 = raw_input(color.CYAN+"Please enter a BMC IPv4 address, e.g:- 10.0.124.119:- "+color.END)

IPv6eth1 = raw_input(color.CYAN+"Please enter a BMC IPv6 address, e.g:- 3001:db8::1:- "+color.END)



print color.PINK+"\n*** NOTE:Before executing this script, Please make sure that  Network is enabled for  eth1 -> Both IPv4 and IPv6 ***"+color.END
              



response = os.system("ping -c 1 " + IPv4eth1)

#and then check the response...
if response == 0:
  print IPv4eth1, color.GREEN+"is up!"+color.END
else:
  print IPv4eth1, color.RED+"is down!"+color.END
  sys.exit()


response = os.system("ping6 -c 1 " + IPv6eth1)

#and then check the response...
if response == 0:
  print IPv6eth1, color.GREEN+"is up!"+color.END
else:
  print IPv6eth1, color.RED+"is down!"+color.END
  sys.exit()






print color.PINK+"\n*********** SUPPORT FOR IPV4 ONLY (IPV6 DISABLED) ************"+color.END




print color.BLUE+"\nGet Device ID Response eth1 IPv4[should get response eth1 IPv4]"+color.END
os.system("ipmitool -H "+IPv4eth1+" -I lanplus -U admin -P admin raw 6 1")

print color.PINK+"******Disable IPV6 Support for eth1********"+color.END
os.system("ipmitool -H "+IPv6eth1+" -I lanplus -U admin -P admin raw 0x0c 0x01 0x08 0x33 0x00")
print color.GREEN+"IPv6 Support was disabled for eth1"+color.END
print color.YELLOW+"Please wait for two minutes:BMC is resetting"+color.END
import time
time.sleep(80)



print color.CYAN+"verify IPv6 Support was disabled for eth1?[should throw error]"+color.END
print color.BLUE+"Get Device ID Response for eth1 IPv6"+color.END
os.system("ipmitool -H "+IPv6eth1+" -I lanplus -U admin -P admin raw 6 1")
print color.BLUE+"Get Device ID Response for eth1 IPv4[should get response]"+color.END
os.system("ipmitool -H "+IPv4eth1+" -I lanplus -U admin -P admin raw 6 1")


if response == 0:
   print response, color.GREEN+"\nIPv4 Support only for eth1 -> PASS"+color.END
else:
     print response, color.RED+"\nIPv4 Support only for eth1 -> FAIL"+color.END
     sys.exit()

print color.PINK+"\n*********** SUPPORT FOR IPV6 ONLY (IPV4 DISABLED) ************"+color.END 

print color.PINK+"***\nEnable IPV6 Support for eth1 ***"+color.END
print color.BLUE+"Get Device ID Response eth1  IPv4 [should get response]"+color.END 
os.system("ipmitool -H "+IPv4eth1+" -I lanplus -U admin -P admin raw 6 1")
print color.PINK+"***\nEnable IPV6 Support for eth1 ***"+color.END

os.system("ipmitool -H "+IPv4eth1+" -I lanplus -U admin -P admin raw 0x0c 0x01 0x08 0x33 0x01")
print color.GREEN+"IPv6 Support was enabled for eth1"+color.END


print color.YELLOW+"Please wait for two minutes:BMC is resetting"+color.END
import time
time.sleep(80)

print color.CYAN+"\nVerify IPv4 support was disabled for eth1 by GET IPv4 Support addressing Enable Command[Response should be 11 01]"+color.END
response = os.system("ipmitool -H "+IPv6eth1+" -I lanplus -U admin -P admin  raw 0x0c 0x02 0x08 0x33 00 00")

print color.CYAN+"verify IPv6 Support was enabled for eth1?[should get response]"+color.END
print color.BLUE+"Get Device ID Response for eth1 IPv6"+color.END
os.system("ipmitool -H  "+IPv6eth1+" -I lanplus -U admin -P admin raw 6 1")
if response == 0:
   print response, color.GREEN+"\nIPv6 Support only for eth1 -> PASS"+color.END
else:
     print response, color.RED+"\nIPv6 Support only for eth1 -> FAIL"+color.END
     sys.exit()

print color.CYAN+"verify IPv4 Support was disabled for eth1?"+color.END
print color.BLUE+"Get Device ID Response eth1 IPv4 [should throw error]"+color.END
os.system("ipmitool -H "+IPv4eth1+" -I lanplus -U admin -P admin raw 6 1")



print color.PINK+"\n*************SUPPORT FOR BOTH  IPV4 and IPv6  ************"+color.END






print color.CYAN+"verify IPv6 Support was enabled for eth1?[should get response]"+color.END 
print color.BLUE+"Get Device ID Response for eth1 IPv6[should get response]"+color.END
os.system("ipmitool -H "+IPv6eth1+" -I lanplus -U admin -P admin raw 6 1")
print color.PINK+"Enable IPv4 and IPv6 Support for eth1"+color.END
os.system("ipmitool -H "+IPv6eth1+" -I lanplus -U admin -P admin raw 0x0c 0x01 0x08 0x33 0x02")
print color.GREEN+"IPv4 and IPv6 Support was enabled for eth1"+color.END 
print color.YELLOW+"Please wait for two minutes:BMC is resetting"+color.END
import time
time.sleep(80)

print color.CYAN+"verify IPv4 and IPv6 Support was enabled for eth1?[should get response]"+color.END
print color.BLUE+"Get Device ID Response for eth1 IPv4 [should get response]"+color.END
os.system("ipmitool -H  "+IPv4eth1+" -I lanplus -U admin -P admin raw 6 1")


print color.BLUE+"Get Device ID Response for eth1 IPv6 [should get response]"+color.END
os.system("ipmitool -H  "+IPv6eth1+" -I lanplus -U admin -P admin raw 6 1")

if response == 0:
   print response, color.GREEN+"\nSupport  for IPv4 and IPv6 for  eth1 -> PASS"+color.END
else:
     print response, color.RED+"\nSupport  for IPv4 and IPv6 for  eth1 -> FAIL"+color.END
     sys.exit()

sys.stdout=open("output.txt","a")


