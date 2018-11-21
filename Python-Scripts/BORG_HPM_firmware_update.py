#!/usr/bin/env python
#-*- coding: utf-8 -*-

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

print color.YELLOW+('Please copy Create HPM Utility,hpmimage.conf and BMC,BIOS,CPLD Firmware images in same directory with name as rom.ima,flash.sec,cpld.jed ')+color.END

ip = raw_input(color.CYAN+"Please enter a BMC IP, e.g:- 10.0.124.119:- "+color.END)




def component0():
#     os.system("cd "+path_logfile+"")
     os.system("sed -i 's/^#//g' hpmimage.conf")
     os.system("sed -i '7,15 s/^/#/' hpmimage.conf")
     os.system("sed -i '17,25 s/^/#/' hpmimage.conf")
     os.system("sed -i '27,35 s/^/#/' hpmimage.conf")
     os.system("sed -i '37,45 s/^/#/' hpmimage.conf")
     os.system("sed -i '57,65 s/^/#/' hpmimage.conf")
     os.system("./CreateHPMImage create hpmimage.conf")
     print(color.GREEN+'Component zero was selected -> Generated HPM image will contain only BOOT Component and it will flash Boot Component'+color.END)
     os.system("ipmitool -H "+ip+" -U admin -P admin -I lanplus hpm upgrade AllComp.hpm component 0 -z 0x7fff") 


def component1():
#     os.system("cd "+path_logfile+"")
     os.system("sed -i 's/^#//g' hpmimage.conf")
     os.system("sed -i '7,15 s/^/#/' hpmimage.conf")
     os.system("sed -i '17,25 s/^/#/' hpmimage.conf")
     os.system("sed -i '27,35 s/^/#/' hpmimage.conf")
     os.system("sed -i '37,45 s/^/#/' hpmimage.conf")
     os.system("sed -i '47,55 s/^/#/' hpmimage.conf")
     os.system("./CreateHPMImage create hpmimage.conf")
     print(color.GREEN+'Component one was selected -> Genearated HPM image will contain only APP Component and it will flash APP Component'+color.END)
     os.system("ipmitool -H "+ip+" -U admin -P admin -I lanplus hpm upgrade AllComp.hpm component 1 -z 0x7fff")

	 
def component2():
#     os.system("cd "+path_logfile+"")
     os.system("sed -i 's/^#//g' hpmimage.conf")
     os.system("sed -i '37,45 s/^/#/' hpmimage.conf")
     os.system("sed -i '17,25 s/^/#/' hpmimage.conf")
     os.system("sed -i '27,35 s/^/#/' hpmimage.conf")
     os.system("sed -i '47,55 s/^/#/' hpmimage.conf")
     os.system("sed -i '57,65 s/^/#/' hpmimage.conf")
     os.system("./CreateHPMImage create hpmimage.conf")
     print(color.GREEN+'Component two was selected -> Genearated HPM image will contain only BIOS Component and it will flash BIOS Component'+color.END)
     os.system("ipmitool -H "+ip+" -U admin -P admin -I lanplus hpm upgrade AllComp.hpm component 2 -z 0x7fff")


	
def component3():
#     os.system("cd "+path_logfile+"")
     os.system("sed -i 's/^#//g' hpmimage.conf")
     os.system("sed -i '7,15 s/^/#/' hpmimage.conf")
     os.system("sed -i '37,45 s/^/#/' hpmimage.conf")
     os.system("sed -i '27,35 s/^/#/' hpmimage.conf")
     os.system("sed -i '47,55 s/^/#/' hpmimage.conf")
     os.system("sed -i '57,65 s/^/#/' hpmimage.conf")
     os.system("./CreateHPMImage create hpmimage.conf")
     print(color.GREEN+'Component three was selected -> Genearated HPM image will contain only BIOSA Component and it will flash BIOSA Component'+color.END)
     os.system("ipmitool -H "+ip+" -U admin -P admin -I lanplus hpm upgrade AllComp.hpm component 3 -z 0x7fff")

	 
def component4():
#     os.system("cd "+path_logfile+"")
     os.system("sed -i 's/^#//g' hpmimage.conf")
     os.system("sed -i '7,15 s/^/#/' hpmimage.conf")
     os.system("sed -i '17,25 s/^/#/' hpmimage.conf")
     os.system("sed -i '37,45 s/^/#/' hpmimage.conf")
     os.system("sed -i '47,55 s/^/#/' hpmimage.conf")
     os.system("sed -i '57,65 s/^/#/' hpmimage.conf")
     os.system("./CreateHPMImage create hpmimage.conf")
     print(color.GREEN+'Component four was selected -> Genearated HPM image will contain only CPLD1 Component and it will flash CPLD1 Component'+color.END)
     os.system("ipmitool -H "+ip+" -U admin -P admin -I lanplus hpm upgrade AllComp.hpm component 4 -z 0x7fff")

def component5():
#     os.system("cd "+path_logfile+"")
     os.system("sed -i 's/^#//g' hpmimage.conf")
     os.system("sed -i '7,15 s/^/#/' hpmimage.conf")
     os.system("sed -i '17,25 s/^/#/' hpmimage.conf")
     os.system("sed -i '27,35 s/^/#/' hpmimage.conf")
     os.system("sed -i '47,55 s/^/#/' hpmimage.conf")
     os.system("sed -i '57,65 s/^/#/' hpmimage.conf")
     os.system("./CreateHPMImage create hpmimage.conf")
     print(color.GREEN+'Component five was selected -> Genearated HPM image will contain only CPLD2 Component and it will flash CPLD2 Component'+color.END)
     os.system("ipmitool -H "+ip+" -U admin -P admin -I lanplus hpm upgrade AllComp.hpm component 5 -z 0x7fff")


	
def component6():
#     os.system("cd "+path_logfile+"")
     os.system("sed -i 's/^#//g' hpmimage.conf")
     os.system("./CreateHPMImage create hpmimage.conf")
     print(color.GREEN+'Component six was selected -> Genearated HPM image will contain All Components such as BOOT,APP,BIOS,BIOS A,CPLD1 and CPLD2 and it will Flash All Components(BOOT,APP,BIOS,BIOS_A,CPLD1,CPLD2...)'+color.END)
     os.system("ipmitool -H "+ip+" -U admin -P admin -I lanplus hpm upgrade AllComp.hpm  -z 0x7fff")


def component7():
#    os.system("cd "+path_logfile+"")
    os.system("sed -i 's/^#//g' hpmimage.conf")
    os.system("sed -i '7,15 s/^/#/' hpmimage.conf")
    os.system("sed -i '17,25 s/^/#/' hpmimage.conf")
    os.system("sed -i '27,35 s/^/#/' hpmimage.conf")
    os.system("sed -i '37,45 s/^/#/' hpmimage.conf")
    os.system("./CreateHPMImage create hpmimage.conf")
    print(color.GREEN+'Component seven was selected -> Genearated HPM image will contain both BMC Components(BOOT,APP) and it will flash both BOOT and APP Components'+color.END)
    os.system("ipmitool -H "+ip+" -U admin -P admin -I lanplus hpm upgrade AllComp.hpm component 0 component 1 -z 0x7fff")


def component8():
#    os.system("cd "+path_logfile+"")
    os.system("sed -i 's/^#//g' hpmimage.conf")
    os.system("sed -i '37,45 s/^/#/' hpmimage.conf")
    os.system("sed -i '47,55 s/^/#/' hpmimage.conf")
    os.system("sed -i '27,35 s/^/#/' hpmimage.conf")
    os.system("sed -i '57,65 s/^/#/' hpmimage.conf")
    os.system("./CreateHPMImage create hpmimage.conf")
    print(color.GREEN+'Component eight was selected -> Genearated HPM image will contain both BIOS Components(BIOS,BIOS A) and it will flash both BIOS Components'+color.GREEN)
    os.system("ipmitool -H "+ip+" -U admin -P admin -I lanplus hpm upgrade AllComp.hpm component 2 component 3 -z 0x7fff")


def component9():
#    os.system("cd "+path_logfile+"")
    os.system("sed -i 's/^#//g' hpmimage.conf")
    os.system("sed -i '7,15 s/^/#/' hpmimage.conf")
    os.system("sed -i '47,55 s/^/#/' hpmimage.conf")
    os.system("sed -i '17,25 s/^/#/' hpmimage.conf")
    os.system("sed -i '57,65 s/^/#/' hpmimage.conf")
    os.system("./CreateHPMImage create hpmimage.conf")
    print(color.GREEN+'Component nine was selected -> Genearated HPM image will contain both CPLD Components(CPLD1,CPLD2) and it will flash both CPLD1 and CPLD2 Components'+color.GREEN)
    os.system("ipmitool -H "+ip+" -U admin -P admin -I lanplus hpm upgrade AllComp.hpm component 4 component 5 -z 0x7fff")
    


x = int(input(color.PINK+"Please enter a number from 1 to 9(0-Only BOOT Component, 1-Only APP Component, 2-BIOS Component, 3-BIOS A Component, 4-CPLD Component 5-CPLD1 Component 6- All Components(BOOT,APP,BIOS,BIOSA,CPLD1,CPLD2) 7-BOOT and APP Component 8- BIOS and BIOS A Component 9- CPLD1 and CPLD2 Component :- "+color.END))

if x == 0:
   component0()
elif x == 1:
   component1()
elif x == 2:
   component2()
elif x == 3:
   component3()
elif x ==4:
   component4()
elif x == 5:
   component5()
elif x == 6:
   component6()
elif x == 7:
   component7()
elif x == 8:
   component8()
elif x == 9:
   component9()
   
else:
   print("Please enter the numbers from 1 to 9")

