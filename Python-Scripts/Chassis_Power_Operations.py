#!/usr/bin/python
import os
import time
import sys
class color:
      GREEN='\033[92m'
      RED='\033[91m'
      END='\033[0m'
      PURPLE='\033[35m'
      YELLOW='\033[93m'
      CYAN='\033[36m'
      PINK='\033[95m'
      BLUE='\033[44m'

IP = raw_input(color.CYAN+"Please enter a BMC IPv4/IPv6 address, e.g:- 10.0.124.119/3001:db8::1 = "+color.END)

n = int(raw_input(color.CYAN+"Enter the number of Chassis Power control(1 count =on and off) iterations ex:- 1000 ="+color.END))


response = os.system("ping -c 1 " + IP)

#and then check the response...
if response == 0:
  print IP, color.GREEN+"is up!"+color.END
else:
  print IP, color.RED+"is down!"+color.END
  sys.exit()

for i in range(1,n):
   os.system("ipmitool -H "+IP+" -I lanplus -U admin -P admin chassis power status")
   print 'Get Device ID:'
   os.system("ipmitool -H "+IP+" -I lanplus -U admin -P admin chassis power on")
   os.system("ipmitool -H "+IP+" -I lanplus -U admin -P admin chassis power status")
   print 'Get Device ID:'
   time.sleep(3)
   os.system("ipmitool -H "+IP+" -I lanplus -U admin -P admin chassis power cycle")
   os.system("yes | ipmitool -H "+IP+" -I lanplus -U admin -P admin chassis power status")
   print 'Get Device ID:'
   time.sleep(3)
   os.system("ipmitool -H "+IP+" -I lanplus -U admin -P admin chassis power status")
   os.system("ipmitool -H "+IP+" -I lanplus -U admin -P admin chassis power off")
   os.system("ipmitool -H "+IP+" -I lanplus -U admin -P admin chassis power status")
   print 'Get Device ID:'
   time.sleep(3)
   os.system("ipmitool -H "+IP+" -I lanplus -U admin -P admin chassis power status")
   print 'The count is:', i 
   

