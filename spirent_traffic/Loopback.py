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

cisco14 = {
	"host": "10.91.126.200",
	"username": "dshaw1",
	"password": "N0@ught33b0y",
	"device_type": "cisco_xr",
	}

F_vlan = 50
def Command_Creation(filename, item1,item2, interface_name):
    with open(filename,'r') as f:
        Temp = f.read()
        failure_command = Template(Temp).render(item = interface_name)
        f.close()
        file_open = open(str(item1)+"_Loop_"+str(item2)+"_command.txt", 'w+')
        file_open.write(failure_command)
        file_open.write('\n')
        file_open.close()

def netmiko_Set_config(item1):
	print("***** log in to device")
	net_connect = Netmiko(**cisco14)
	f = open(str(item1)+"_Loop_Set_command.txt",'r')
	f2 = f.readlines()
	output = net_connect.send_config_set(f2)
	net_connect.commit()
	print(output)
	net_connect.exit_config_mode()
	net_connect.disconnect()

def netmiko_Release_config(item1):
	print("***** log in to device")
	net_connect = Netmiko(**cisco14)
	f = open(str(item1)+"_Loop_Release_command.txt",'r')
	f2 = f.readlines()
	output = net_connect.send_config_set(f2)
	net_connect.commit()
	print(output)
	net_connect.exit_config_mode()
	net_connect.disconnect()


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
		log_level                                        = '0');

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
		action                                           = 'enable');

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
port_list = ['11/6','11/10']
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

int_ret0 = sth.interface_config (
		mode                                             = 'config',
		port_handle                                      = port_handle[0],
		create_host                                      = 'false',
		intf_mode                                        = 'ethernet',
		phy_mode                                         = 'fiber',
		scheduling_mode                                  = 'RATE_BASED',
		port_loadunit                                    = 'PERCENT_LINE_RATE',
		port_load                                        = '10',
		enable_ping_response                             = '0',
		control_plane_mtu                                = '1500',
		flow_control                                     = 'false',
		speed                                            = 'ether1000',
		data_path_mode                                   = 'normal',
		autonegotiation                                  = '1');

status = int_ret0['status']
if (status == '0') :
	print("run sth.interface_config failed")
	print(int_ret0)
else:
	print("***** run sth.interface_config AR13 successfully")

int_ret1 = sth.interface_config (
		mode                                             = 'config',
		port_handle                                      = port_handle[1],
		create_host                                      = 'false',
		intf_mode                                        = 'ethernet',
		phy_mode                                         = 'fiber',
		scheduling_mode                                  = 'RATE_BASED',
		port_loadunit                                    = 'PERCENT_LINE_RATE',
		port_load                                        = '10',
		enable_ping_response                             = '0',
		control_plane_mtu                                = '1500',
		flow_control                                     = 'false',
		speed                                            = 'ether1000',
		data_path_mode                                   = 'normal',
		autonegotiation                                  = '1');

status = int_ret1['status']
if (status == '0') :
	print("run sth.interface_config failed")
	print(int_ret1)
else:
	print("***** run sth.interface_config AR14 successfully")


##############################################################
#create device and config the protocol on it
##############################################################

#start to create the device: FF_Type_13
device_ret0 = sth.emulation_device_config (
		mode                                             = 'create',
		ip_version                                       = 'ipv4',
		encapsulation                                    = 'ethernet_ii_vlan',
		port_handle                                      = port_handle[0],
		vlan_user_pri                                    = '0',
		vlan_cfi                                         = '0',
		vlan_id                                          = F_vlan,
		vlan_tpid                                        = '33024',
		vlan_id_repeat_count                             = '0',
		vlan_id_step                                     = '0',
		router_id                                        = '192.0.1.13',
		count                                            = '1',
		enable_ping_response                             = '0',
		mac_addr                                         = '00:10:94:00:01:13',
		mac_addr_step                                    = '00:00:00:00:00:01',
		intf_ip_addr                                     = '10.0.1.13',
		intf_prefix_len                                  = '24',
		resolve_gateway_mac                              = 'true',
		gateway_ip_addr                                  = '10.0.1.14',
		gateway_ip_addr_step                             = '0.0.0.0',
		intf_ip_addr_step                                = '0.0.0.1');

status = device_ret0['status']
if (status == '0') :
	print("run sth.emulation_device_config failed")
	print(device_ret0)
else:
	print("***** run sth.emulation_device_config FF_Type_13 successfully")

#start to create the device: XX_Type_13
device_ret1 = sth.emulation_device_config (
		mode                                             = 'create',
		ip_version                                       = 'ipv4',
		encapsulation                                    = 'ethernet_ii_vlan',
		port_handle                                      = port_handle[0],
		vlan_user_pri                                    = '0',
		vlan_cfi                                         = '0',
		vlan_id                                          = '49',
		vlan_tpid                                        = '33024',
		vlan_id_repeat_count                             = '0',
		vlan_id_step                                     = '0',
		router_id                                        = '192.0.2.13',
		count                                            = '1',
		enable_ping_response                             = '0',
		mac_addr                                         = '00:10:94:00:02:13',
		mac_addr_step                                    = '00:00:00:00:00:01',
		intf_ip_addr                                     = '10.0.2.13',
		intf_prefix_len                                  = '24',
		resolve_gateway_mac                              = 'true',
		gateway_ip_addr                                  = '10.0.2.14',
		gateway_ip_addr_step                             = '0.0.0.0',
		intf_ip_addr_step                                = '0.0.0.1');

status = device_ret1['status']
if (status == '0') :
	print("run sth.emulation_device_config failed")
	print(device_ret1)
else:
	print("***** run sth.emulation_device_config XX_Type_13 successfully")

#start to create the device: FY_Type_13
device_ret2 = sth.emulation_device_config (
		mode                                             = 'create',
		ip_version                                       = 'ipv4',
		encapsulation                                    = 'ethernet_ii_vlan',
		port_handle                                      = port_handle[0],
		vlan_user_pri                                    = '0',
		vlan_cfi                                         = '0',
		vlan_id                                          = '49',
		vlan_tpid                                        = '33024',
		vlan_id_repeat_count                             = '0',
		vlan_id_step                                     = '0',
		router_id                                        = '192.0.3.13',
		count                                            = '1',
		enable_ping_response                             = '0',
		mac_addr                                         = '00:10:94:00:03:13',
		mac_addr_step                                    = '00:00:00:00:00:01',
		intf_ip_addr                                     = '10.0.3.13',
		intf_prefix_len                                  = '24',
		resolve_gateway_mac                              = 'true',
		gateway_ip_addr                                  = '10.0.3.14',
		gateway_ip_addr_step                             = '0.0.0.0',
		intf_ip_addr_step                                = '0.0.0.1');

status = device_ret2['status']
if (status == '0') :
	print("run sth.emulation_device_config failed")
	print(device_ret2)
else:
	print("***** run sth.emulation_device_config FY_Type_13 successfully")

#start to create the device: FF-Type_14
device_ret3 = sth.emulation_device_config (
		mode                                             = 'create',
		ip_version                                       = 'ipv4',
		encapsulation                                    = 'ethernet_ii_vlan',
		port_handle                                      = port_handle[1],
		vlan_user_pri                                    = '0',
		vlan_cfi                                         = '0',
		vlan_id                                          = F_vlan,
		vlan_tpid                                        = '33024',
		vlan_id_repeat_count                             = '0',
		vlan_id_step                                     = '0',
		router_id                                        = '192.0.1.14',
		count                                            = '1',
		enable_ping_response                             = '0',
		mac_addr                                         = '00:10:94:00:01:14',
		mac_addr_step                                    = '00:00:00:00:00:01',
		intf_ip_addr                                     = '10.0.1.14',
		intf_prefix_len                                  = '24',
		resolve_gateway_mac                              = 'true',
		gateway_ip_addr                                  = '10.0.1.13',
		gateway_ip_addr_step                             = '0.0.0.0',
		intf_ip_addr_step                                = '0.0.0.1');

status = device_ret3['status']
if (status == '0') :
	print("run sth.emulation_device_config failed")
	print(device_ret3)
else:
	print("***** run sth.emulation_device_config FF-Type_14 successfully")

#start to create the device: XX-Type_14
device_ret4 = sth.emulation_device_config (
		mode                                             = 'create',
		ip_version                                       = 'ipv4',
		encapsulation                                    = 'ethernet_ii_vlan',
		port_handle                                      = port_handle[1],
		vlan_user_pri                                    = '0',
		vlan_cfi                                         = '0',
		vlan_id                                          = '50',
		vlan_tpid                                        = '33024',
		vlan_id_repeat_count                             = '0',
		vlan_id_step                                     = '0',
		router_id                                        = '192.0.2.14',
		count                                            = '1',
		enable_ping_response                             = '0',
		mac_addr                                         = '00:10:94:00:02:14',
		mac_addr_step                                    = '00:00:00:00:00:01',
		intf_ip_addr                                     = '10.0.2.14',
		intf_prefix_len                                  = '24',
		resolve_gateway_mac                              = 'true',
		gateway_ip_addr                                  = '10.0.2.13',
		gateway_ip_addr_step                             = '0.0.0.0',
		intf_ip_addr_step                                = '0.0.0.1');

status = device_ret4['status']
if (status == '0') :
	print("run sth.emulation_device_config failed")
	print(device_ret4)
else:
	print("***** run sth.emulation_device_config XX-Type_14 successfully")

#start to create the device: FY-Type_14
device_ret5 = sth.emulation_device_config (
		mode                                             = 'create',
		ip_version                                       = 'ipv4',
		encapsulation                                    = 'ethernet_ii_qinq',
		port_handle                                      = port_handle[1],
		vlan_user_pri                                    = '0',
		vlan_cfi                                         = '0',
		vlan_id                                          = '49',
		vlan_tpid                                        = '33024',
		vlan_id_repeat_count                             = '0',
		vlan_id_step                                     = '0',
		vlan_outer_id_repeat_count                       = '0',
		vlan_outer_user_pri                              = '0',
		vlan_outer_id_step                               = '0',
		vlan_outer_tpid                                  = '34984',
		vlan_outer_cfi                                   = '0',
		vlan_outer_id                                    = '50',
		router_id                                        = '192.0.3.14',
		count                                            = '1',
		enable_ping_response                             = '0',
		mac_addr                                         = '00:10:94:00:03:14',
		mac_addr_step                                    = '00:00:00:00:00:01',
		intf_ip_addr                                     = '10.0.3.14',
		intf_prefix_len                                  = '24',
		resolve_gateway_mac                              = 'true',
		gateway_ip_addr                                  = '10.0.3.13',
		gateway_ip_addr_step                             = '0.0.0.0',
		intf_ip_addr_step                                = '0.0.0.1');

status = device_ret5['status']
if (status == '0') :
	print("run sth.emulation_device_config failed")
	print(device_ret5)
else:
	print("***** run sth.emulation_device_config FY-Type_14 successfully")


##############################################################
#create traffic
##############################################################

streamblock_ret1 = sth.traffic_config (
		mode                                             = 'create',
		port_handle                                      = port_handle[0],
		l2_encap                                         = 'ethernet_ii_vlan',
		mac_src                                          = '00:10:94:00:01:13',
		mac_dst                                          = '00:10:94:00:01:13',
		vlan_cfi                                         = '0',
		vlan_tpid                                        = '33024',
		vlan_id                                          = F_vlan,
		vlan_user_priority                               = '0',
		enable_control_plane                             = '0',
		l3_length                                        = '9078',
		name                                             = 'StreamBlock_F-F',
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
		rate_mbps                                        = '100');

status = streamblock_ret1['status']
if (status == '0') :
	print("run sth.traffic_config failed")
	print(streamblock_ret1)
else:
	print("***** run sth.traffic_config StreamBlock_F-F on AR13 successfully")

streamblock_ret2 = sth.traffic_config (
		mode                                             = 'create',
		port_handle                                      = port_handle[0],
		l2_encap                                         = 'ethernet_ii_vlan',
		mac_src                                          = '00:10:94:00:02:13',
		mac_dst                                          = '00:10:94:00:02:13',
		vlan_outer_cfi                                   = '0',
		vlan_outer_tpid                                  = '33024',
		vlan_outer_user_priority                         = '0',
		vlan_id_outer                                    = '49',
		vlan_cfi                                         = '0',
		vlan_tpid                                        = '33024',
		vlan_id                                          = '50',
		vlan_user_priority                               = '0',
		enable_control_plane                             = '0',
		l3_length                                        = '9074',
		name                                             = 'StreamBlock_X-X',
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
		rate_mbps                                        = '100');

status = streamblock_ret2['status']
if (status == '0') :
	print("run sth.traffic_config failed")
	print(streamblock_ret2)
else:
	print("***** run sth.traffic_config StreamBlock_X-X on AR13 successfully")

streamblock_ret3 = sth.traffic_config (
		mode                                             = 'create',
		port_handle                                      = port_handle[0],
		l2_encap                                         = 'ethernet_ii_vlan',
		mac_src                                          = '00:10:94:00:03:13',
		mac_dst                                          = '00:10:94:00:03:13',
		vlan_cfi                                         = '0',
		vlan_tpid                                        = '33024',
		vlan_id                                          = '49',
		vlan_user_priority                               = '0',
		enable_control_plane                             = '0',
		l3_length                                        = '9078',
		name                                             = 'StreamBlock_F-Y',
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
		rate_mbps                                        = '100');

status = streamblock_ret3['status']
if (status == '0') :
	print("run sth.traffic_config failed")
	print(streamblock_ret3)
else:
	print("***** run sth.traffic_config StreamBlock_F-Y on AR13 successfully")

streamblock_ret4 = sth.traffic_config (
		mode                                             = 'create',
		port_handle                                      = port_handle[1],
		l2_encap                                         = 'ethernet_ii_vlan',
		mac_src                                          = '00:10:94:00:03:14',
		mac_dst                                          = '00:10:94:00:03:14',
		vlan_outer_cfi                                   = '0',
		vlan_outer_tpid                                  = '34984',
		vlan_outer_user_priority                         = '0',
		vlan_id_outer                                    = '50',
		vlan_cfi                                         = '0',
		vlan_tpid                                        = '33024',
		vlan_id                                          = '49',
		vlan_user_priority                               = '0',
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
		rate_mbps                                        = '100');

status = streamblock_ret4['status']
if (status == '0') :
	print("run sth.traffic_config failed")
	print(streamblock_ret4)
else:
	print("***** run sth.traffic_config StreamBlock_Y-F on AR14 successfully")

#config part is finished

##############################################################
#start devices
##############################################################

List1 = ['L1','L2']
List2 = ['Set','Release']

interface_name = 'GigabitEthernet0/0/0/11'
for item1 in List1:
	for item2 in List2:
		Command_Creation("tem_"+item1+"_Loop_"+item2+"_command.j2", item1,item2 , interface_name)
		print("**** Templateing Done for "+str(item1)+" & "+ str(item2)+" command")



for item1 in List1:

	print("**** perform "+str(item1)+" Loop ")
	netmiko_Set_config(item1)
	pprint(streamblock_ret1['stream_id'])
	FF_stream = streamblock_ret1['stream_id']
	traffic_ctrl_ret = sth.traffic_control (
            stream_handle                                      = [FF_stream],
            action                                           = 'run',
            duration                                         = '30')
    
	status = traffic_ctrl_ret['status']
	if (status == '0') :
		print("run sth.traffic_control failed")
		print(traffic_ctrl_ret)
	else:
		print("***** run sth.traffic started successfully")

    ##############################################################
    #start to get the device results
    ##############################################################

    ##############################################################
    #start to get the traffic results
    ##############################################################

	traffic_results_ret = sth.traffic_stats (
			port_handle                                      = [port_handle[0],port_handle[1]],
			streams =  [FF_stream],
			mode                                             = 'detailed_streams');

	status = traffic_results_ret['status']
	if (status == '0') :
		print("run sth.traffic_stats failed")
		print(traffic_results_ret)
	else:
		print("***** run sth.traffic_stats successfully, and results is:")
		pprint(traffic_results_ret)

	rx = traffic_results_ret[port_handle[0]]['stream'][FF_stream]['rx']['0']['total_pkts']
	tx = traffic_results_ret[port_handle[0]]['stream'][FF_stream]['tx']['0']['total_pkts']

	print("**** No of Rx packets are: " + str(rx))
	print("**** No of Tx packets are: " + str(tx))
	if tx == rx :
		print(" ***************** Test has Passed")
	else:
		print(" ***************** Test has Failed")

	raffic_ctrl_ret = sth.traffic_control(
		port_handle=[port_handle[0], port_handle[1]],
		action='clear_stats');

	print("**** Release "+str(item1)+" Loop ")
	netmiko_Release_config(item1)
	time.sleep(30)

##############################################################
#clean up the session, release the ports reserved and cleanup the dbfile
##############################################################

cleanup_sta = sth.cleanup_session (
		port_handle                                      = [port_handle[0],port_handle[1]],
		clean_dbfile                                     = '1');

status = cleanup_sta['status']
if (status == '0') :
	print("run sth.cleanup_session failed")
	print(cleanup_sta)
else:
	print("***** run sth.cleanup_session successfully")

print("**************Finish***************")
