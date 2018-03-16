import subprocess
import libvirt
import re
import xml.etree.ElementTree as ET
import random
from xml.dom import minidom

conn = libvirt.open('qemu:///system')
if conn == None:
    raise Exception('Failed to open connection to the hypervisor')

try:  
    domains = conn.listDomainsID()
except:
    raise Exception('Failed to find any domains')


hashMap = {}
for domain_id in domains:
    this_vm = conn.lookupByID(domain_id)
    xmlDesc =  this_vm.XMLDesc(0)
    vm_name = this_vm.name()
    fileName ="/etc/libvirt/qemu/"+vm_name+".xml"
    tree = ET.parse(fileName)
    root = tree.getroot()
    for mac in root.iter('mac'):
           print(this_vm.name())
           vm_name = this_vm.name()
           list = mac.attrib
           print(mac.attrib)
           macAddress= list['address']
           print("****")
           if macAddress in hashMap:
                print "********Duplicate found********* "+macAddress
                randomNumber = random.randint(1,9)
                macAddress= macAddress[:16]+str(randomNumber)
                print("Updated mac address " +str(macAddress))
                mac.set('address',macAddress)
                tree.write(fileName)
                #iface = conn.interfaceDefineXML(this_vm.XMLDesc(0), 0)
           hashMap[macAddress]=1


print(hashMap)
