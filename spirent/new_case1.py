##############################################################
#Loading HLTAPI for Python
##############################################################
from __future__ import print_function
import sth
import time
from pprint import pprint

##############################################################
#config the parameters for the logging
##############################################################

test_sta = sth.test_config (
		log                                              = '1',
		logfile                                          = 'new_case1_logfile',
		vendorlogfile                                    = 'new_case1_stcExport',
		vendorlog                                        = '1',
		hltlog                                           = '1',
		hltlogfile                                       = 'new_case1_hltExport',
		hlt2stcmappingfile                               = 'new_case1_hlt2StcMapping',
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
port_list = ['7/7','7/8']
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
		transmit_clock_source                            = 'INTERNAL',
		flow_control                                     = 'false',
		deficit_idle_count                               = 'false',
		pfc_negotiate_by_dcbx                            = '0',
		speed                                            = 'ether10000',
		data_path_mode                                   = 'normal',
		port_mode                                        = 'LAN',
		autonegotiation                                  = '1',
		duplex                                           = 'full');

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
		scheduling_mode                                  = 'RATE_BASED',
		port_loadunit                                    = 'PERCENT_LINE_RATE',
		port_load                                        = '10',
		enable_ping_response                             = '0',
		control_plane_mtu                                = '1500',
		transmit_clock_source                            = 'INTERNAL',
		flow_control                                     = 'false',
		deficit_idle_count                               = 'false',
		pfc_negotiate_by_dcbx                            = '0',
		speed                                            = 'ether10000',
		data_path_mode                                   = 'normal',
		port_mode                                        = 'LAN',
		autonegotiation                                  = '1',
		duplex                                           = 'full');

status = int_ret1['status']
if (status == '0') :
	print("run sth.interface_config failed")
	print(int_ret1)
else:
	print("***** run sth.interface_config successfully")


##############################################################
#create device and config the protocol on it
##############################################################


##############################################################
#create traffic
##############################################################

streamblock_ret1 = sth.traffic_config (
		mode                                             = 'create',
		port_handle                                      = port_handle[0],
		l2_encap                                         = 'ethernet_ii_vlan',
		mac_src                                          = '00:10:94:00:00:06',
		mac_dst                                          = '00:10:94:00:00:05',
		vlan_outer_cfi                                   = '0',
		vlan_outer_tpid                                  = '34984',
		vlan_outer_user_priority                         = '0',
		vlan_id_outer                                    = '1400',
		vlan_cfi                                         = '0',
		vlan_tpid                                        = '33024',
		vlan_id                                          = '1400',
		vlan_user_priority                               = '0',
		enable_control_plane                             = '0',
		l3_length                                        = '1474',
		name                                             = 'StreamBlock_6',
		fill_type                                        = 'constant',
		fcs_error                                        = '0',
		fill_value                                       = '0',
		frame_size                                       = '1500',
		traffic_state                                    = '1',
		high_speed_result_analysis                       = '1',
		length_mode                                      = 'fixed',
		tx_port_sending_traffic_to_self_en               = 'false',
		disable_signature                                = '0',
		enable_stream_only_gen                           = '1',
		pkts_per_burst                                   = '1',
		inter_stream_gap_unit                            = 'bytes',
		inter_stream_gap                                 = '12',
		rate_pps                                         = '1000');

status = streamblock_ret1['status']
if (status == '0') :
	print("run sth.traffic_config failed")
	print(streamblock_ret1)
else:
	print("***** run sth.traffic_config successfully")

streamblock_ret2 = sth.traffic_config (
		mode                                             = 'create',
		port_handle                                      = port_handle[1],
		l2_encap                                         = 'ethernet_ii_vlan',
		mac_src                                          = '00:10:94:00:00:05',
		mac_dst                                          = '00:10:94:00:00:06',
		vlan_outer_cfi                                   = '0',
		vlan_outer_tpid                                  = '34984',
		vlan_outer_user_priority                         = '0',
		vlan_id_outer                                    = '1400',
		vlan_cfi                                         = '0',
		vlan_tpid                                        = '33024',
		vlan_id                                          = '1400',
		vlan_user_priority                               = '0',
		enable_control_plane                             = '0',
		l3_length                                        = '1474',
		name                                             = 'StreamBlock_7',
		fill_type                                        = 'constant',
		fcs_error                                        = '0',
		fill_value                                       = '0',
		frame_size                                       = '1500',
		traffic_state                                    = '1',
		high_speed_result_analysis                       = '1',
		length_mode                                      = 'fixed',
		tx_port_sending_traffic_to_self_en               = 'false',
		disable_signature                                = '0',
		enable_stream_only_gen                           = '1',
		pkts_per_burst                                   = '1',
		inter_stream_gap_unit                            = 'bytes',
		inter_stream_gap                                 = '12',
		rate_pps                                         = '1000');

status = streamblock_ret2['status']
if (status == '0') :
	print("run sth.traffic_config failed")
	print(streamblock_ret2)
else:
	print("***** run sth.traffic_config successfully")

#config part is finished

##############################################################
#start devices
##############################################################


##############################################################
#start traffic
##############################################################

traffic_ctrl_ret = sth.traffic_control (
		port_handle                                      = [port_handle[0],port_handle[1]],
		action                                           = 'run',
		duration                                         = '60');

status = traffic_ctrl_ret['status']
if (status == '0') :
	print("run sth.traffic_control failed")
	print(traffic_ctrl_ret)
else:
	print("***** run sth.traffic_control successfully")


##############################################################
#start to get the device results
##############################################################

time.sleep(60)
##############################################################
#start to get the traffic results
##############################################################

traffic_results_ret = sth.traffic_stats (
		port_handle                                      = [port_handle[0],port_handle[1]],
		mode                                             = 'all');

status = traffic_results_ret['status']
if (status == '0') :
	print("run sth.traffic_stats failed")
	pprint(traffic_results_ret)
else:
	print("***** run sth.traffic_stats successfully, and results is:")
	pprint(traffic_results_ret)


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
