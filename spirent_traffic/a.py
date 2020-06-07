from __future__ import print_function
import time
from jinja2 import Template
import os
cisco14 = {
	"host": "10.91.126.200",
	"username": "dshaw1",
	"password": "N0@ught33b0y",
	"device_type": "cisco_xr",
	}

F_vlan = 50
interface_name = 'GigabitEthernet0/0/0/11'
file_path = os.path.dirname(os.path.realpath(__file__))

print(file_path)

def Command_Creation(filename, item1,item2, interface_name):
	dict_to_render = {
	'main_inf': interface_name,
	'sub_if': F_vlan
	}
	with open(filename,'r') as f:
		Temp = f.read()
		failure_command = Template(Temp).render(**dict_to_render)
		f.close()
		file_open = open(file_path + "/commands/" + str(item1)+"_Loop_"+str(item2)+"_command.txt", 'w+')
		file_open.write(failure_command)
		file_open.write('\n')
		file_open.close()

List1 = ['L1','L2']
List2 = ['Set','Release']

for item1 in List1:
	for item2 in List2:
		location = file_path + "/templates/"+"tem_"+item1+"_Loop_"+item2+"_command.j2"
		Command_Creation(location, item1,item2 , interface_name)
		print("**** Templateing Done for "+str(item1)+" & "+ str(item2)+" command")