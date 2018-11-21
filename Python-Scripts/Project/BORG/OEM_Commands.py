#! / usr/bin/python3
# -*- coding: utf-8 -*-


import time
import os
import sys
import fileinput



class color:
      GREEN='\033[92m'
      RED='\033[91m'
      END='\033[0m'
      PURPLE='\033[35m'
      YELLOW='\033[93m'
      CYAN='\033[36m'
      PINK='\033[95m'
      BLUE='\033[44m'  



n = int(raw_input(color.CYAN+"Enter the number of iterations for HPM fw update ex:- 1000 ="+color.END))

IPv4eth1 = raw_input(color.CYAN+"Please enter a BMC IPv4 address, e.g:- 10.0.124.119:- "+color.END)

IPv6eth1 = raw_input(color.CYAN+"Please enter a BMC IPv4 address, e.g:- 3000:db8::1 =>"+color.END)

print color.PINK+"\n*** NOTE:Before executing this script, Please make sure that Host is UP and Thermal,IPMB limit is set as 1 ***"+color.END
              



response = os.system("ping -c 1 " + IPv4eth1)

#and then check the response...
if response == 0:
  print IPv4eth1, color.GREEN+"is up!"+color.END
else:
  print IPv4eth1, color.RED+"is down!"+color.END
  sys.exit()

for i in range(1,n):

   print color.PINK+"\n*********** GET DEVICE ID M3 (OEM) ************"+color.END

   print color.BLUE+"\nIPv4 -> Get Device ID Response for Vulcan ID0 [Response should be like -> 00 01 06 00 02 01 d1 b3 00 00 00 00 00 00 00]  "+color.END
   os.system("ipmitool -H "+IPv4eth1+" -I lanplus -U admin -P admin raw 0x3a 0xD 0")

   print color.PINK+"******IPv6 -> Get Device ID Response for Vulcan ID0 [Response should be like -> 00 01 06 00 02 01 d1 b3 00 00 00 00 00 00 00] ********"+color.END
   os.system("ipmitool -H "+IPv6eth1+" -I lanplus -U admin -P admin raw 0x3a 0xD 0")

   print color.BLUE+"\nIPv4 -> Get Device ID Response for Vulcan ID1 [Response should be like -> 00 01 06 00 02 01 d1 b3 00 00 00 00 00 00 00] "+color.END
   os.system("ipmitool -H "+IPv4eth1+" -I lanplus -U admin -P admin raw 0x3a 0xD 1")

   print color.PINK+"******IPv6 -> Get Device ID Response for Vulcan ID1 [Response should be like -> 00 01 06 00 02 01 d1 b3 00 00 00 00 00 00 00] ********"+color.END
   os.system("ipmitool -H "+IPv6eth1+" -I lanplus -U admin -P admin raw 0x3a 0xD 1")

   print color.PINK+"\n*********** GET CHIP TEMPERATURE (OEM) ************"+color.END

   print color.BLUE+"\nIPv4 -> Get chip temperature for Vulcan ID0 [Response should be d1 b3 00 38 31 00 ]  "+color.END
   os.system("ipmitool -H "+IPv4eth1+" -I lanplus -U admin -P admin raw 0x3a 0x24 0 0xd1 0xb3 0x00")

   print color.PINK+"******IPv6 -> Get chip temperature for Vulcan ID0 [Response should be d1 b3 00 38 31 00 ] ********"+color.END
   os.system("ipmitool -H "+IPv6eth1+" -I lanplus -U admin -P admin raw 0x3a 0x24 0 0xd1 0xb3 0x00")

   print color.BLUE+"\nIPv4 ->  Get chip temperature Response for Vulcan ID1 [Response should be d1 b3 00 38 31 00 ]   "+color.END
   os.system("ipmitool -H "+IPv4eth1+" -I lanplus -U admin -P admin raw 0x3a 0x24 1 0xd1 0xb3 0x00")

   print color.PINK+"******IPv6 -> Get chip temperature for Vulcan ID1 [Response should be d1 b3 00 38 31 00 ] ********"+color.END
   os.system("ipmitool -H "+IPv6eth1+" -I lanplus -U admin -P admin raw 0x3a 0x24 1 0xd1 0xb3 0x00")

   print color.PINK+"\n*********** SET and GET IOAD  ************"+color.END

   print color.BLUE+"\nIPv4 -> Set IOAD Via IPv6 address[Response should be d1 b3 00]  "+color.END
   os.system("ipmitool -H "+IPv4eth1+" -I lanplus -U admin -P admin raw 0x3a 0x9 0xd1 0xb3 00 0x1 0x2 0x3 0x4 0x5 0x6 0x7 0x8")

   print color.PINK+"******IPv6 -> Get IOAD Via IPv6 address[Response should be d1 b3 00 01 02 03 04 05 06 07 08] ********"+color.END
   os.system("ipmitool -H "+IPv6eth1+" -I lanplus -U admin -P admin raw 0x3a 0x10 0xd1 0xb3 00")

   print color.BLUE+"\nIPv4 ->  Set IOAD Via IPv4 address[Response should be d1 b3 00]   "+color.END
   os.system("ipmitool -H "+IPv4eth1+" -I lanplus -U admin -P admin raw 0x3a 0x9 0xd1 0xb3 00 0x15 0x24 0x32 0x46 0x75 0x63 0x73 0x34")

   print color.PINK+"******IPv6 -> Get IOAD Via IPv4 address[Response should be d1 b3 00 0x15 0x24 0x32 0x46 0x75 0x63 0x73 0x34] ********"+color.END
   os.system("ipmitool -H "+IPv6eth1+" -I lanplus -U admin -P admin raw 0x3a 0x10 0xd1 0xb3 00")

   print color.BLUE+"\nIPv4 ->  Set IOAD Via IPv4 address[Response should be given data is invalid]   "+color.END
   os.system("ipmitool -H "+IPv4eth1+" -I lanplus -U admin -P admin raw 0x3a 0x9 0xd1 0xb3 00 0x15 0x24 0x32 0x46 0x75 0xfd 0x73 0xp")

   print color.PINK+"******IPv6 -> Get IOAD Via IPv4 address[Response should be d1 b3 00 0x15 0x24 0x32 0x46 0x75 0x63 0x73 0x34] ********"+color.END
   os.system("ipmitool -H "+IPv6eth1+" -I lanplus -U admin -P admin raw 0x3a 0x10 0xd1 0xb3 00")

   print color.PINK+"\n*********** SET PLATFORM MODE  ************"+color.END

   print color.BLUE+"\nIPv4 -> Set Single MS MODE IPv4[Response: There should not be an error] "+color.END
   os.system("ipmitool -H "+IPv4eth1+" -I lanplus -U admin -P admin raw 0x3a 0x12 0x00")

   print color.PINK+"******IPv6 -> Set DUAL_LMM_MODE IPv6[Response: There should not be an error] ********"+color.END
   os.system("ipmitool -H "+IPv6eth1+" -I lanplus -U admin -P admin raw 0x3a 0x12 0x01")

   print color.BLUE+"\nIPv4 ->  Set SINGLE_MS_VA_MSTR IPv4 [Response: There should not be an error]  "+color.END
   os.system("ipmitool -H "+IPv4eth1+" -I lanplus -U admin -P admin raw 0x3a 0x12 0x02")

   print color.PINK+"******IPv6 -> Set DUAL_LMM_VA_ONLY IPv6[Response: There should not be an error]********"+color.END
   os.system("ipmitool -H "+IPv6eth1+" -I lanplus -U admin -P admin raw 0x3a 0x12 0x03")

   print color.BLUE+"\nIPv4 ->  Set DUAL_LMM_VB_ONLY IPv4 [Response: There should not be an error]  "+color.END
   os.system("ipmitool -H "+IPv4eth1+" -I lanplus -U admin -P admin raw 0x3a 0x12 0x04")

   print color.PINK+"******IPv6 -> Set Invalid Platform mode IPv6 [Response: There should not be an error] ********"+color.END
   os.system("ipmitool -H "+IPv6eth1+" -I lanplus -U admin -P admin raw 0x3a 0x12 0x05")

   print color.PINK+"\n*********** GET CHIP THROTTLE (OEM) ************"+color.END

   print color.BLUE+"\nIPv4 -> Get chip throttle for Vulcan ID0 [Response should be like d1 b3 00 52 03 c9 ]  "+color.END
   os.system("ipmitool -H "+IPv4eth1+" -I lanplus -U admin -P admin raw 0x3a 0x25 0 0xd1 0xb3 0x00")

   print color.PINK+"******IPv6 -> Get chip throttle for Vulcan ID0 [Response should be like d1 b3 00 52 03 c9 ] ********"+color.END
   os.system("ipmitool -H "+IPv6eth1+" -I lanplus -U admin -P admin raw 0x3a 0x25 0 0xd1 0xb3 0x00")

   print color.BLUE+"\nIPv4 ->  Get chip throttle Response for Vulcan ID1 [Response should be like d1 b3 00 52 03 c9 ]   "+color.END
   os.system("ipmitool -H "+IPv4eth1+" -I lanplus -U admin -P admin raw 0x3a 0x25 1 0xd1 0xb3 0x00")

   print color.PINK+"******IPv6 -> Get chip throttle Vulcan ID1 [Response should be like d1 b3 00 52 03 c9 ] ********"+color.END
   os.system("ipmitool -H "+IPv6eth1+" -I lanplus -U admin -P admin raw 0x3a 0x25 1 0xd1 0xb3 0x00")
   
   print color.GREEN+'The count is:'+color.END, i
