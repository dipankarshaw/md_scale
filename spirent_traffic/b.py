from __future__ import print_function
import time
from jinja2 import Template
from netmiko import Netmiko
import os
cisco5 = {
	"host": "10.91.126.115",
	"username": "dshaw1",
	"password": "N0@ught33b0y",
	"device_type": "cisco_xr",
	}

cisco6 = {
	"host": "10.91.126.116",
	"username": "dshaw1",
	"password": "N0@ught33b0y",
	"device_type": "cisco_xr",
	}

def netmiko_Set_config(item1,device):
	print("***** log in to device")
	net_connect = Netmiko(**device)
	f = open(file_path + "/commands/" + str(item1)+"_shut_noshut_command.txt",'r')
	f2 = f.readlines()
	output = net_connect.send_config_set(f2)
	net_connect.commit()
	print(output)
	net_connect.exit_config_mode()
	net_connect.disconnect()

file_path = os.path.dirname(os.path.realpath(__file__))

print(file_path)

def Command_Creation(filename, item1, interface_name):
	dict_to_render = {
	'main_inf': interface_name
	}
	with open(filename,'r') as f:
		Temp = f.read()
		failure_command = Template(Temp).render(**dict_to_render)
		f.close()
		file_open = open(file_path + "/commands/" + str(item1)+"_shut_noshut_command.txt", 'w+')
		file_open.write(failure_command)
		file_open.write('\n')
		file_open.close()

List1 = ['AR5','AR6']
interface_name = ['TenGigE0/0/1/3/2','TenGigE0/0/0/19']
for item1 in List1:
	location = file_path + "/templates/"+"tem_shut_noshut.j2"
	if item1 == 'AR5':
		interface = interface_name[0]
	else:
		interface = interface_name[1]
	
	Command_Creation(location, item1, interface)
	print("**** Templateing Done for "+str(item1)+ "command")

for item1 in List1:

	print("**** perform "+str(item1)+" commannds ")
	device ={}
	if item1 == 'AR5':
		device = cisco5
	else:
		device = cisco6
	netmiko_Set_config(item1,device)
