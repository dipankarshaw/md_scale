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


def dip():

    ##############################################################
    #config the parameters for the logging
    ##############################################################

    test_sta = sth.test_config (
            log                                              = '1',
            logfile                                          = 'dip2_logfile',
            vendorlogfile                                    = 'dip2_stcExport',
            vendorlog                                        = '1',
            hltlog                                           = '1',
            hltlogfile                                       = 'dip2_hltExport',
            hlt2stcmappingfile                               = 'dip2_hlt2StcMapping',
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
    port_list = ['11/8','4/6']
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
            vlan_user_pri                                    = '7',
            vlan_cfi                                         = '0',
            vlan_id                                          = '20',
            vlan_tpid                                        = '33024',
            vlan_id_repeat_count                             = '0',
            vlan_id_step                                     = '0',
            router_id                                        = '192.0.0.5',
            count                                            = '1',
            enable_ping_response                             = '1',
            mac_addr                                         = '00:10:94:00:00:05',
            mac_addr_step                                    = '00:00:00:00:00:01',
            intf_ip_addr                                     = '192.168.10.1',
            intf_prefix_len                                  = '24',
            resolve_gateway_mac                              = 'true',
            gateway_ip_addr                                  = '192.168.10.2',
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
            vlan_user_pri                                    = '7',
            vlan_cfi                                         = '0',
            vlan_id                                          = '20',
            vlan_tpid                                        = '33024',
            vlan_id_repeat_count                             = '0',
            vlan_id_step                                     = '0',
            router_id                                        = '192.0.0.6',
            count                                            = '1',
            enable_ping_response                             = '1',
            mac_addr                                         = '00:10:94:00:00:06',
            mac_addr_step                                    = '00:00:00:00:00:01',
            intf_ip_addr                                     = '192.168.10.2',
            intf_prefix_len                                  = '24',
            resolve_gateway_mac                              = 'true',
            gateway_ip_addr                                  = '192.168.10.1',
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
            l3_length                                        = '9100',
            name                                             = 'StreamBlock_18-3',
            fill_type                                        = 'constant',
            fcs_error                                        = '0',
            fill_value                                       = '0',
            frame_size                                       = '9100',
            traffic_state                                    = '1',
            high_speed_result_analysis                       = '1',
            length_mode                                      = 'fixed',
            dest_port_list                                   = ['port2','port1'],
            tx_port_sending_traffic_to_self_en               = 'false',
            disable_signature                                = '0',
            enable_stream_only_gen                           = '1',
            pkts_per_burst                                   = '1',
            inter_stream_gap_unit                            = 'bytes',
            inter_stream_gap                                 = '12',
            rate_mbps                                        = '50',
            mac_discovery_gw                                 = '192.168.10.2');

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
            l3_length                                        = '9100',
            name                                             = 'StreamBlock_18-4',
            fill_type                                        = 'constant',
            fcs_error                                        = '0',
            fill_value                                       = '0',
            frame_size                                       = '9100',
            traffic_state                                    = '1',
            high_speed_result_analysis                       = '1',
            length_mode                                      = 'fixed',
            dest_port_list                                   = ['port2','port1'],
            tx_port_sending_traffic_to_self_en               = 'false',
            disable_signature                                = '0',
            enable_stream_only_gen                           = '1',
            pkts_per_burst                                   = '1',
            inter_stream_gap_unit                            = 'bytes',
            inter_stream_gap                                 = '12',
            rate_mbps                                        = '50',
            mac_discovery_gw                                 = '192.168.10.1');

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
            duration                                         = '30');

    status = traffic_ctrl_ret['status']
    if (status == '0') :
        print("run sth.traffic_control failed")
        print(traffic_ctrl_ret)
    else:
        print("***** run sth.traffic_control successfully")


    ##############################################################
    #start to get the device results
    ##############################################################


    ##############################################################
    #start to get the traffic results
    ##############################################################

    traffic_results_ret = sth.traffic_stats (
            port_handle                                      = [port_handle[0],port_handle[1]],
            mode                                             = 'all');

    status = traffic_results_ret['status']
    if (status == '0') :
        print("run sth.traffic_stats failed")
        print(traffic_results_ret)
    else:
        print("***** run sth.traffic_stats successfully, and results is:")
        print(traffic_results_ret)


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

    result = SpirentResult(traffic_results_ret, port_list)
    return result



def SpirentResult(traffic_results_ret, port_list):

    ##############################################################
    #Get required values from Stats
    ##############################################################

    traffic_result = str(traffic_results_ret)

    #regex to get rx, tx and streams from traffic_results_ret
    RX = '(streamblock\d+)\S+\s+\S+(rx)\S+\s+\S+total_pkt_bytes\S+\s+\S(\d+)'
    TX = '(streamblock\d+).*?(tx)\S+\s+\S+total_pkt_bytes\S+\s+\S(\d+)'
    StreamBlock = 'streamblock\d+'


    print('Spirent Ports= ' + str(port_list) + '\nTotal Ports= ' + str(len(port_list)))
    PortStatus = 'Spirent Ports= ' + str(port_list) + '\nTotal Ports= ' + str(len(port_list))

    StreamBlock = re.findall(StreamBlock, traffic_result)
    print('Stream Configured= ' + str(StreamBlock) + '\nTotal Streams= ' + str(len(StreamBlock)))
    StreamStatus = 'Stream Configured= ' + str(StreamBlock) + '\nTotal Streams= ' + str(len(StreamBlock))

    rx_stats = re.findall(RX, traffic_result)
    tx_stats = re.findall(TX, traffic_result)

    print('rx_stats= ' + str(rx_stats))
    print('tx_stats= ' + str(tx_stats))

    stats = 'rx_stats= ' + str(rx_stats) + '\ntx_stats= ' + str(tx_stats)

    StreamResult = []

    for i in range(0,len(StreamBlock)):
        if rx_stats[i][2] == tx_stats[i][2]:
            print(str(rx_stats[i][0] + ' = pass'))
            StreamResult.append('pass')

        else:
            print(str(rx_stats[i][0] + ' = fail'))
            StreamResult.append('fail')

    print(str(StreamResult))

    OverallStatus = '\n' + PortStatus + '\n' + StreamStatus + '\n' + stats + '\n' + str(StreamResult)
    print(OverallStatus)

    return OverallStatus


dip()
