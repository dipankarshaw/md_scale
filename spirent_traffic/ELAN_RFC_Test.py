##############################################################
#Loading HLTAPI for Python
##############################################################
from __future__ import print_function
import sth
import time
import json
import os
import sys
import re
from pprint import pprint

list1 = [1518,9100]
list2 = [80,90,100]


##############################################################
#config the parameters for the logging
##############################################################

test_sta = sth.test_config (
		log                                              = '1',
		logfile                                          = 'ELAN_RFC_Test_logfile',
		vendorlogfile                                    = 'ELAN_RFC_Test_stcExport',
		vendorlog                                        = '1',
		hltlog                                           = '1',
		hltlogfile                                       = 'ELAN_RFC_Test_hltExport',
		hlt2stcmappingfile                               = 'ELAN_RFC_Test_hlt2StcMapping',
		hlt2stcmapping                                   = '1',
		log_level                                        = '7');

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
		scheduling_mode                                  = 'PORT_BASED',
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
	print("***** run sth.interface_config successfully")

int_ret1 = sth.interface_config (
		mode                                             = 'config',
		port_handle                                      = port_handle[1],
		create_host                                      = 'false',
		intf_mode                                        = 'ethernet',
		phy_mode                                         = 'fiber',
		scheduling_mode                                  = 'PORT_BASED',
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
	print("***** run sth.interface_config successfully")


##############################################################
#create device and config the protocol on it
##############################################################

#start to create the device: Device 1
device_ret0 = sth.emulation_device_config (
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
		router_id                                        = '192.0.0.3',
		count                                            = '1',
		enable_ping_response                             = '0',
		mac_addr                                         = '00:10:94:00:00:13',
		mac_addr_step                                    = '00:00:00:00:00:01',
		intf_ip_addr                                     = '10.0.0.13',
		intf_prefix_len                                  = '24',
		resolve_gateway_mac                              = 'true',
		gateway_ip_addr                                  = '10.0.0.14',
		gateway_ip_addr_step                             = '0.0.0.0',
		intf_ip_addr_step                                = '0.0.0.1');

status = device_ret0['status']
if (status == '0') :
	print("run sth.emulation_device_config failed")
	print(device_ret0)
else:
	print("***** run sth.emulation_device_config successfully")

#start to create the device: Device 2
device_ret1 = sth.emulation_device_config (
		mode                                             = 'create',
		ip_version                                       = 'ipv4',
		encapsulation                                    = 'ethernet_ii_vlan',
		port_handle                                      = port_handle[1],
		vlan_user_pri                                    = '0',
		vlan_cfi                                         = '0',
		vlan_id                                          = '49',
		vlan_tpid                                        = '33024',
		vlan_id_repeat_count                             = '0',
		vlan_id_step                                     = '0',
		router_id                                        = '192.0.0.4',
		count                                            = '1',
		enable_ping_response                             = '0',
		mac_addr                                         = '00:10:94:00:00:14',
		mac_addr_step                                    = '00:00:00:00:00:01',
		intf_ip_addr                                     = '10.0.0.14',
		intf_prefix_len                                  = '24',
		resolve_gateway_mac                              = 'true',
		gateway_ip_addr                                  = '10.0.0.13',
		gateway_ip_addr_step                             = '0.0.0.0',
		intf_ip_addr_step                                = '0.0.0.1');

status = device_ret1['status']
if (status == '0') :
	print("run sth.emulation_device_config failed")
	print(device_ret1)
else:
	print("***** run sth.emulation_device_config successfully")


##############################################################
#create traffic
##############################################################

src_hdl = device_ret0['handle'].split()[0]

dst_hdl = device_ret1['handle'].split()[0]


streamblock_ret1 = sth.traffic_config (
		mode                                             = 'create',
		port_handle                                      = port_handle[0],
		emulation_src_handle                             = src_hdl,
		emulation_dst_handle                             = dst_hdl,
		l3_protocol                                      = 'ipv4',
		ip_id                                            = '0',
		ip_ttl                                           = '255',
		ip_hdr_length                                    = '5',
		ip_protocol                                      = '253',
		ip_fragment_offset                               = '0',
		ip_mbz                                           = '0',
		ip_precedence                                    = '6',
		ip_tos_field                                     = '0',
		enable_control_plane                             = '0',
		l3_length                                        = '128',
		name                                             = 'StreamBlock_3-3',
		fill_type                                        = 'constant',
		fcs_error                                        = '0',
		fill_value                                       = '0',
		frame_size                                       = '128',
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
		rate_percent                                     = '10',
		mac_discovery_gw                                 = '10.0.0.14');

status = streamblock_ret1['status']
if (status == '0') :
	print("run sth.traffic_config failed")
	print(streamblock_ret1)
else:
	print("***** run sth.traffic_config successfully")

src_hdl = device_ret1['handle'].split()[0]

dst_hdl = device_ret0['handle'].split()[0]


streamblock_ret2 = sth.traffic_config (
		mode                                             = 'create',
		port_handle                                      = port_handle[1],
		emulation_src_handle                             = src_hdl,
		emulation_dst_handle                             = dst_hdl,
		l3_protocol                                      = 'ipv4',
		ip_id                                            = '0',
		ip_ttl                                           = '255',
		ip_hdr_length                                    = '5',
		ip_protocol                                      = '253',
		ip_fragment_offset                               = '0',
		ip_mbz                                           = '0',
		ip_precedence                                    = '6',
		ip_tos_field                                     = '0',
		enable_control_plane                             = '0',
		l3_length                                        = '128',
		name                                             = 'StreamBlock_3-4',
		fill_type                                        = 'constant',
		fcs_error                                        = '0',
		fill_value                                       = '0',
		frame_size                                       = '128',
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
		rate_percent                                     = '10',
		mac_discovery_gw                                 = '10.0.0.13');

status = streamblock_ret2['status']
if (status == '0') :
	print("run sth.traffic_config failed")
	print(streamblock_ret2)
else:
	print("***** run sth.traffic_config successfully")

##############################################################
#do MAC learning & clear stats
##############################################################

print("***** sending 30 sec initial traffic for mac-learning")
traffic_ctrl_ret = sth.traffic_control(
	port_handle=[port_handle[0], port_handle[1]],
	action='run',
	duration='30');
time.sleep(5)
traffic_ctrl_ret = sth.traffic_control(
	port_handle=[port_handle[0], port_handle[1]],
	action='stop')
print("***** mac learning done")
print("***** clear the stats stats of the Traffic")
traffic_ctrl_ret = sth.traffic_control(
	port_handle=[port_handle[0], port_handle[1]],
	action='clear_stats');
time.sleep(10)

##############################################################
#start RFC test
##############################################################

streamblock_handle = [streamblock_ret1['stream_id'],streamblock_ret2['stream_id']]

rfc_cfg0 = sth.test_rfc2544_config (
		mode                                             = 'create',
		test_type                                        = 'throughput',
		streamblock_handle                               = streamblock_handle,
		endpoint_creation                                = '0',
		frame_size_mode                                  = 'custom',
		start_traffic_delay                              = '2',
		resolution                                       = '1',
		learning_mode                                    = 'l3',
		rate_upper_limit                                 = '100',
		frame_size                                       = ['1518','9100'],
		enable_latency_threshold                         = '0',
		enable_detailresults                             = '1',
		rate_step                                        = '10',
		stagger_start_delay                              = '0',
		learning_frequency                               = 'learn_once',
		enable_jitter_measure                            = '0',
		delay_after_transmission                         = '15',
		ignore_limit                                     = '0',
		enable_cyclic_resolution                         = '1',
		test_duration_mode                               = 'seconds',
		back_off                                         = '50',
		iteration_count                                  = '1',
		rate_lower_limit                                 = '1',
		accept_frame_loss                                = '1',
		test_duration                                    = '60',
		enable_learning                                  = '1',
		latency_type                                     = 'LILO',
		search_mode                                      = 'step',
		enable_seq_threshold                             = '0',
		l3_learning_retry_count                          = '5',
		initial_rate                                     = '80');

status = rfc_cfg0['status']
if (status == '0') :
	print("run sth.test_rfc2544_config failed")
	print(rfc_cfg0)
else:
	print("***** run sth.test_rfc2544_config successfully")

#config part is finished

##############################################################
#start devices
##############################################################

ctrl_ret1 = sth.test_rfc2544_control (
		action                                           = 'run',
		wait                                             = '1');

status = ctrl_ret1['status']
if (status == '0') :
	print("run sth.test_rfc2544_control failed")
	print(ctrl_ret1)
else:
	print("***** run sth.test_rfc2544_control successfully")


##############################################################
#start to get the device results
##############################################################

results_ret1 = sth.test_rfc2544_info (
		test_type                                        = 'throughput',
		clear_result                                     = '0',
        enable_load_detail                               = '1');

status = results_ret1['status']
if (status == '0') :
	print("run sth.test_rfc2544_info failed")
	print(results_ret1)
else:
	print("***** run sth.test_rfc2544_info successfully, and results is:")
	pprint(results_ret1)

Short_result = results_ret1['rfc2544throughput']['load_detail']['iteration']['1']['frame_size']
for item1 in list1:
    for item2 in list2:
        print ("***** frame loss for Frame size " 
        + str(item1) 
        + str(" and load ") 
        + str(item2) 
        + str(" is ") 
        + str(Short_result[str(item1)][str(item2)]['frame_loss']))


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
