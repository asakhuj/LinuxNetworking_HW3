import subprocess
import libvirt
import re
import xml.etree.ElementTree as ET
import random
from xml.dom import minidom

print("Question 3 : Part 3 : Multiple hypervisors")
hypervisorList =  {}
num = raw_input("Enter how many hypervisors you wish to connect to :")
print("Enter the IP address and root user name")
for i in range(int(num)):
    IP = raw_input("IP : ")
    rootUser = raw_input("Root user name : ")
    hypervisorList[IP]= rootUser

#print(hypervisorList)
hashMap={}

for key,value in hypervisorList.iteritems() :
     print(key +" " +value)
     conn = libvirt.open("qemu+ssh://"+value+"@"+key+"/system")
     if conn == None:
	     raise Exception('Failed to open connection to the hypervisor')
     try:  
         domains = conn.listDomainsID()
     except:
         raise Exception('Failed to find any domains')
     for domain_id in domains:
           this_vm = conn.lookupByID(domain_id)
           xmlDesc =  this_vm.XMLDesc(0)
           vm_name = this_vm.name()
           fileName ="/etc/libvirt/qemu/"+vm_name+".xml"
           tree = ET.parse(fileName)
    	   root = tree.getroot()
    	   for mac in root.iter('mac'):
                vm_name = this_vm.name()
                list = mac.attrib
                macAddress= list['address']
                print("-------------------------------------------------------------------")
                print(vm_name +" : " +macAddress)
                print("-------------------------------------------------------------------")
                if macAddress in hashMap:
                     print "WARNING********Duplicate MAC address found ********* "+vm_name
                hashMap[macAddress]=1
