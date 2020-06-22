##############################################################
#Loading HLTAPI for Python
##############################################################
from __future__ import print_function
import sth
import time
import json
import os
import sys
import yaml
import re
from pprint import pprint
from netmiko import Netmiko
import datetime
from genie import testbed
from jinja2 import Template
import csv

deviceA = {
	"host": "10.91.126.115",
	"username": "dshaw1",
	"password": "N0@ught33b0y",
	"device_type": "cisco_xr",
	}
deviceB = {
	"host": "10.91.126.201",
	"username": "dshaw1",
	"password": "N0@ught33b0y",
	"device_type": "cisco_xr",
	}
port_list = ['7/8','7/7']
interface_name = {
	"deviceA" : 'TenGigE 0/0/1/3/2',
	"deviceB" : 'TenGigE 0/0/0/5'
}

device_list = [deviceA,deviceB]
file_path = os.path.dirname(os.path.realpath(__file__))
F_vlan = 50
deviceA_X_VLAN = 51
deviceB_X_VLAN = 50
deviceA_Y_VLAN = [51,50]
deviceB_F_VLAN = 50
traffic_rate = 8000
port_speed = 'ether10000'  #ether1000,ether10000
copper_fiber = 'fiber' #copper,fiber
mac = {
	"DMAC": '00:10:94:00:01:13',
	"SMAC": '00:10:94:00:01:13'
}
List1 = ['L1','L2']
List2 = ['Set','Release']
inter_exter_list = ['internal','external','line']
loop_id = 1
dict_result = {}
interface_name_list = []
for k,v in interface_name.items():
	interface_name_list.append(v)


def get_L2_loop_ID(show_output):
	show_output_list = show_output.split(" ")
	return show_output_list[-1]

	
def command_ouput():
	print("**** statistic of traffic on both devices")
	for uni_port,device in zip(interface_name_list,device_list):
		net_connect = Netmiko(**device)
		command = 'show policy-map interface {}.{} | utility egrep "Match\|input\|output\|Drop"'.format(uni_port,F_vlan)
		command_ouput = net_connect.send_command("show run hostname")
		command_ouput += net_connect.send_command(command)
		print(command_ouput)
		net_connect.disconnect()

def clear_QOS_ouput():
	print("**** clearing statistic on both devices")
	for uni_port,device in zip(interface_name_list,device_list):
		net_connect = Netmiko(**device)
		command = 'clear qos counters interface {}.{}'.format(uni_port,F_vlan)
		command_ouput = net_connect.send_command(command)
		print(command_ouput)
		net_connect.disconnect()
	

def Command_Creation(filename, item1,item2,inter_exter,loop_id,**interface_name):
	if inter_exter == 'internal':
		dict_to_render = {
		'main_inf': interface_name['deviceB'],
		'sub_if': F_vlan,
		'internal_external': inter_exter,
		'Loop_id': loop_id
		}
	else:
		dict_to_render = {
		'main_inf': interface_name['deviceA'],
		'sub_if': F_vlan,
		'internal_external': inter_exter,
		'Loop_id': loop_id
		}
	with open(filename,'r') as f:
		Temp = f.read()
		failure_command = Template(Temp).render(**dict_to_render)
		f.close()
		file_open = open(file_path + "/commands/" + str(item1)+"_Loop_"+str(inter_exter)+"_"+str(item2)+"_command.txt", 'w+')
		file_open.write(failure_command)
		file_open.write('\n')
		file_open.close()

def netmiko_Set_config(item1,inter_exter):
	if inter_exter == 'internal':
		net_connect = Netmiko(**deviceB)
		print('***** log in to device {}'.format(deviceB['host']))
	else:
		net_connect = Netmiko(**deviceA)
		print('***** log in to device {}'.format(deviceA['host']))
	f = open(file_path + "/commands/" + str(item1)+"_Loop_"+str(inter_exter)+"_Set_command.txt",'r')
	f2 = f.readlines()
	clear_QOS_ouput()
	output = net_connect.send_config_set(f2)
	net_connect.commit()
	net_connect.exit_config_mode()
	print(output)
	command = "show ethernet loopback active | include ID"
	show_output = net_connect.send_command(command)
	if item1 == "L2":
		loop_id_to_render = get_L2_loop_ID(show_output)
		if loop_id_to_render != "1":
			print("**** doing rendering one more time")
			Command_Creation(location, item1,item2,inter_exter,loop_id_to_render,**interface_name)
	net_connect.disconnect()

def netmiko_Release_config(item1,inter_exter):
	if inter_exter == 'internal':
		net_connect = Netmiko(**deviceB)
		print('***** log in to device {}'.format(deviceB['host']))
	else:
		net_connect = Netmiko(**deviceA)
		print('***** log in to device {}'.format(deviceA['host']))
	f = open(file_path + "/commands/" + str(item1)+"_Loop_"+str(inter_exter)+"_Release_command.txt",'r')
	f2 = f.readlines()
	time.sleep(15)
	command_ouput()
	output = net_connect.send_config_set(f2)
	net_connect.commit()
	net_connect.exit_config_mode()
	print(output)
	net_connect.disconnect()

def spirent_traffic(steam_name,item1,inter_exter):
	stream = steam_name['stream_id']
	traffic_ctrl_ret = sth.traffic_control (
			stream_handle = [stream],
			action = 'run',
			traffic_start_mode = 'sync',
			duration = '30')

	status = traffic_ctrl_ret['status']
	if (status == '0') :
		print("run sth.traffic_control failed")
		print(traffic_ctrl_ret)
	else:
		print("***** run sth.traffic started successfully")

	traffic_results_ret = sth.traffic_stats (
			port_handle                                      = [port_handle[0],port_handle[1]],
			mode                                             = 'all')

	traffic_results_ret1 = sth.traffic_stats (
			port_handle = [port_handle[0],port_handle[1]],
			streams = [stream],
			mode = 'detailed_streams')

	status = traffic_results_ret['status']
	if (status == '0') :
		print("run sth.traffic_stats failed")
		print(traffic_results_ret)
	else:
		print("***** run sth.traffic_stats successfully, and results is:")
		#pprint(traffic_results_ret)
		#pprint(traffic_results_ret1)
	
	deviceA_tx = traffic_results_ret[port_handle[0]]['aggregate']['tx']['pkt_count']
	deviceA_rx = traffic_results_ret[port_handle[0]]['aggregate']['rx']['pkt_count']
	deviceB_tx = traffic_results_ret[port_handle[1]]['aggregate']['tx']['pkt_count']
	deviceB_rx = traffic_results_ret[port_handle[1]]['aggregate']['rx']['pkt_count']
	if deviceA_rx == deviceA_tx:
		print("***************** " + str(item1) +" "+ str(inter_exter) + "Test has Passed")
		print("**** No of Rx packets on deviceA are: " + str(deviceA_rx))
		print("**** No of Tx packets on deviceA are: " + str(deviceA_tx))
		test_result = 'Passed'
	elif deviceB_rx == deviceA_tx:
		print("***************** " + str(item1) +" "+ str(inter_exter)+ "Test has failed")
		print("**** No of Rx packets on deviceB are: " + str(deviceB_rx))
		print("**** No of Tx packets on deviceA are: " + str(deviceA_tx))
		print("**** No of Rx packets on deviceA are: " + str(deviceA_rx))
		print("**** No of Tx packets on deviceB are: " + str(deviceB_tx))
		test_result = 'Failed'
	else:
		print("something wrong")
	
	dict_name = '{}_{}_result'.format(item1,inter_exter)
	dict_local = {}
	dict_local['deviceA_tx'] = deviceA_tx
	dict_local['deviceA_rx'] = deviceA_rx
	dict_local['deviceB_tx'] = deviceB_tx
	dict_local['deviceB_rx'] = deviceB_rx
	dict_local['result'] = test_result
	dict_local['Traffic_rate'] = traffic_rate
	dict_result[dict_name] = dict_local

	traffic_ctrl_ret = sth.traffic_control(
	port_handle=[port_handle[0], port_handle[1]],
	action='clear_stats')



##############################################################
#config the parameters for the logging
##############################################################

test_sta = sth.test_config (
		log                                              = '0',
		logfile                                          = 'Loopback_logfile',
		vendorlogfile                                    = 'Loopback_stcExport',
		vendorlog                                        = '0',
		hltlog                                           = '1',
		hltlogfile                                       = 'Loopback_hltExport',
		hlt2stcmappingfile                               = 'Loopback_hlt2StcMapping',
		hlt2stcmapping                                   = '1',
		log_level                                        = '0')

status = test_sta['status']
if (status == '0') :
	print("run sth.test_config failed")
	print(test_sta)
else:
	print("***** run sth.test_config successfully")


##############################################################
#config the parameters for optimization and parsing
##############################################################

test_ctrl_sta = sth.test_control (
		action                                           = 'enable')

status = test_ctrl_sta['status']
if (status == '0') :
	print("run sth.test_control failed")
	print(test_ctrl_sta)
else:
	print("***** run sth.test_control successfully")


##############################################################
#connect to chassis and reserve port list
##############################################################

i = 0
device = "10.91.113.124"
port_handle = []
intStatus = sth.connect (
		device                                           = device,
		port_list                                        = port_list,
		break_locks                                      = 1,
		offline                                          = 0 )

status = intStatus['status']

if (status == '1') :
	for port in port_list :
		port_handle.append(intStatus['port_handle'][device][port])
		print("\n reserved ports",port,":", port_handle[i])
		i += 1
else :
	print("\nFailed to retrieve port handle!\n")
	print(port_handle)


##############################################################
#interface config
##############################################################
if port_speed =="ether1000":
	for i in range(2):
		interface = 'int_ret_{}'.format(i)
		interface = sth.interface_config (
				mode                                             = 'config',
				port_handle                                      = port_handle[i],
				create_host                                      = 'false',
				intf_mode                                        = 'ethernet',
				phy_mode                                         = copper_fiber,
				scheduling_mode                                  = 'RATE_BASED',
				port_loadunit                                    = 'PERCENT_LINE_RATE',
				port_load                                        = '10',
				enable_ping_response                             = '0',
				control_plane_mtu                                = '1500',
				flow_control                                     = 'false',
				speed                                            = port_speed,
				data_path_mode                                   = 'normal',
				autonegotiation                                  = '1')

		status = interface['status']
		if (status == '0') :
			print("run sth.interface_config failed")
			print(interface)
		else:
			print('***** run sth.interface_config deviceA_{} successfully with 1G speed'.format(i))
else:
	for i in range(2):
		interface = 'int_ret_{}'.format(i)
		interface = sth.interface_config (
				mode                                             = 'config',
				port_handle                                      = port_handle[i],
				create_host                                      = 'false',
				intf_mode                                        = 'ethernet',
				phy_mode                                         = copper_fiber,
				scheduling_mode                                  = 'RATE_BASED',
				port_loadunit                                    = 'PERCENT_LINE_RATE',
				port_load                                        = '10',
				enable_ping_response                             = '0',
				control_plane_mtu                                = '1500',
				flow_control                                     = 'false',
				speed                                            = port_speed,
				data_path_mode                                   = 'normal',
				autonegotiation                                  = '1',
				duplex                                           = 'full')

		status = interface['status']
		if (status == '0') :
			print("run sth.interface_config failed")
			print(interface)
		else:
			print('***** run sth.interface_config deviceA_{} successfully with 10G speed'.format(i))	


# streamblock_retFF = sth.traffic_config (
# 		mode                                             = 'create',
# 		port_handle                                      = port_handle[0],
# 		l2_encap                                         = 'ethernet_ii_vlan',
# 		mac_src                                          = mac['SMAC'],
# 		mac_dst                                          = mac['DMAC'],
# 		vlan_cfi                                         = '0',
# 		vlan_tpid                                        = '33024',
# 		vlan_id                                          = F_vlan,
# 		vlan_user_priority                               = '2',
# 		enable_control_plane                             = '0',
# 		l3_length                                        = '9078',
# 		name                                             = 'StreamBlock_F-F',
# 		fill_type                                        = 'constant',
# 		fcs_error                                        = '0',
# 		fill_value                                       = '0',
# 		frame_size                                       = '9100',
# 		traffic_state                                    = '1',
# 		high_speed_result_analysis                       = '1',
# 		length_mode                                      = 'fixed',
# 		tx_port_sending_traffic_to_self_en               = 'false',
# 		disable_signature                                = '0',
# 		enable_stream_only_gen                           = '1',
# 		pkts_per_burst                                   = '1',
# 		inter_stream_gap_unit                            = 'bytes',
# 		burst_loop_count                                 = '30',
# 		transmit_mode                                    = 'continuous',
# 		inter_stream_gap                                 = '12',
# 		rate_mbps                                        = traffic_rate)

# status = streamblock_retFF['status']
# if (status == '0') :
# 	print("run sth.traffic_config failed")
# 	print(streamblock_retFF)
# else:
# 	print("***** run sth.traffic_config StreamBlock_F-F on DeviceA successfully")

# streamblock_retXX = sth.traffic_config (
# 		mode                                             = 'create',
# 		port_handle                                      = port_handle[0],
# 		l2_encap                                         = 'ethernet_ii_vlan',
# 		mac_src                                          = mac['SMAC'],
# 		mac_dst                                          = mac['DMAC'],
# 		vlan_outer_cfi                                   = '0',
# 		vlan_outer_tpid                                  = '33024',
# 		vlan_outer_user_priority                         = '2',
# 		vlan_id_outer                                    = deviceA_X_VLAN,
# 		vlan_cfi                                         = '0',
# 		vlan_tpid                                        = '33024',
# 		vlan_id                                          = deviceB_X_VLAN,
# 		vlan_user_priority                               = '2',
# 		enable_control_plane                             = '0',
# 		l3_length                                        = '9074',
# 		name                                             = 'StreamBlock_X-X',
# 		fill_type                                        = 'constant',
# 		fcs_error                                        = '0',
# 		fill_value                                       = '0',
# 		frame_size                                       = '9100',
# 		traffic_state                                    = '1',
# 		high_speed_result_analysis                       = '1',
# 		length_mode                                      = 'fixed',
# 		tx_port_sending_traffic_to_self_en               = 'false',
# 		disable_signature                                = '0',
# 		enable_stream_only_gen                           = '1',
# 		pkts_per_burst                                   = '1',
# 		inter_stream_gap_unit                            = 'bytes',
# 		burst_loop_count                                 = '30',
# 		transmit_mode                                    = 'continuous',
# 		inter_stream_gap                                 = '12',
# 		rate_mbps                                        = traffic_rate);

# status = streamblock_retXX['status']
# if (status == '0') :
# 	print("run sth.traffic_config failed")
# 	print(streamblock_retXX)
# else:
# 	print("***** run sth.traffic_config StreamBlock_X-X on DeviceA successfully")

# streamblock_ret3 = sth.traffic_config (
# 		mode                                             = 'create',
# 		port_handle                                      = port_handle[0],
# 		l2_encap                                         = 'ethernet_ii_vlan',
# 		mac_src                                          = mac['SMAC'],
# 		mac_dst                                          = mac['DMAC'],
# 		vlan_cfi                                         = '0',
# 		vlan_tpid                                        = '33024',
# 		vlan_id                                          = sideA_F_VLAN,
# 		vlan_user_priority                               = '0',
# 		enable_control_plane                             = '0',
# 		l3_length                                        = '9078',
# 		name                                             = 'StreamBlock_F-Y',
# 		fill_type                                        = 'constant',
# 		fcs_error                                        = '0',
# 		fill_value                                       = '0',
# 		frame_size                                       = '9100',
# 		traffic_state                                    = '1',
# 		high_speed_result_analysis                       = '1',
# 		length_mode                                      = 'fixed',
# 		tx_port_sending_traffic_to_self_en               = 'false',
# 		disable_signature                                = '0',
# 		enable_stream_only_gen                           = '1',
# 		pkts_per_burst                                   = '1',
# 		inter_stream_gap_unit                            = 'bytes',
# 		burst_loop_count                                 = '30',
# 		transmit_mode                                    = 'continuous',
# 		inter_stream_gap                                 = '12',
# 		rate_mbps                                        = traffic_rate);

# status = streamblock_ret3['status']
# if (status == '0') :
# 	print("run sth.traffic_config failed")
# 	print(streamblock_ret3)
# else:
# 	print("***** run sth.traffic_config StreamBlock_F-Y on AR13 successfully")

streamblock_retYF = sth.traffic_config (
		mode                                             = 'create',
		port_handle                                      = port_handle[0],
		l2_encap                                         = 'ethernet_ii_vlan',
		mac_src                                          = mac['SMAC'],
		mac_dst                                          = mac['DMAC'],
		vlan_outer_cfi                                   = '0',
		vlan_outer_tpid                                  = '34984',
		vlan_outer_user_priority                         = '2',
		vlan_id_outer                                    = deviceA_Y_VLAN[0],
		vlan_cfi                                         = '0',
		vlan_tpid                                        = '33024',
		vlan_id                                          = deviceA_Y_VLAN[1],
		vlan_user_priority                               = '2',
		enable_control_plane                             = '0',
		l3_length                                        = '9074',
		name                                             = 'StreamBlock_Y-F',
		fill_type                                        = 'constant',
		fcs_error                                        = '0',
		fill_value                                       = '0',
		frame_size                                       = '9100',
		traffic_state                                    = '1',
		high_speed_result_analysis                       = '1',
		length_mode                                      = 'fixed',
		tx_port_sending_traffic_to_self_en               = 'false',
		disable_signature                                = '0',
		enable_stream_only_gen                           = '1',
		pkts_per_burst                                   = '1',
		inter_stream_gap_unit                            = 'bytes',
		burst_loop_count                                 = '30',
		transmit_mode                                    = 'continuous',
		inter_stream_gap                                 = '12',
		rate_mbps                                        = traffic_rate);

status = streamblock_retYF['status']
if (status == '0') :
	print("run sth.traffic_config failed")
	print(streamblock_retYF)
else:
	print("***** run sth.traffic_config StreamBlock_Y-F on deviceA successfully")

#config part is finished

##############################################################
#start devices
##############################################################

for item1 in List1:
	if item1 == "L2":
		inter_exter_list = ['internal','external']
	else:
		inter_exter_list = ['internal','external','line']
	for inter_exter in inter_exter_list:
		for item2 in List2:
			location = file_path + "/templates/"+"tem_"+item1+"_Loop_"+item2+"_command.j2"
			Command_Creation(location, item1,item2,inter_exter,loop_id, **interface_name)
			print("**** Templateing Done for "+str(item1)+" "+str(inter_exter)+" & "+ str(item2)+" command")

for item1 in List1:
	if item1 == "L2":
		inter_exter_list = ['internal','external']
	else:
		inter_exter_list = ['internal','external','line']	
	for inter_exter in inter_exter_list:
		print("**** perform "+str(item1)+" "+str(inter_exter)+" Loop ")
		netmiko_Set_config(item1,inter_exter)
		spirent_traffic(streamblock_retFF,item1,inter_exter)
		print("**** Release "+str(item1)+" "+str(inter_exter)+" Loop ")
		netmiko_Release_config(item1,inter_exter)
		time.sleep(30)


##############################################################
#clean up the session, release the ports reserved and cleanup the dbfile
##############################################################

cleanup_sta = sth.cleanup_session (
		port_handle                                      = [port_handle[0],port_handle[1]],
		clean_dbfile                                     = '1')

status = cleanup_sta['status']
if (status == '0') :
	print("run sth.cleanup_session failed")
	print(cleanup_sta)
else:
	print("***** run sth.cleanup_session successfully")

print("**************Finish***************")
# csv_columns = ['Test_name','DeviceA_tx','DeviceA_rx','DeviceB_tx','DeviceB_rx','Pass_Fail']
# csv_file = "Names.csv"
# try:
#     with open(csv_file, 'w') as csvfile:
#         writer = csv.DictWriter(csvfile, fieldnames=csv_columns)
#         writer.writeheader()
#         for k,v in dict_result.items():
#             writer.writerow(k)
# except IOError:
#     print("I/O error")
print(json.dumps(dict_result,indent=4))
