import subprocess
import libvirt
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
           vm_name = this_vm.name()
           list = mac.attrib
           macAddress= list['address']
           print("-------------------------------------------------------------------")
           print(vm_name +" : " +macAddress)
           print("-------------------------------------------------------------------")
           if macAddress in hashMap:
                print "WARNING********Duplicate MAC address found ********* "+vm_name
           hashMap[macAddress]=1
