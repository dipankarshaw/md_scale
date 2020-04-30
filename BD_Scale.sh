#!/bin/sh
echo "
+ Create 50 ELAN service with HQOS, Without CCM,DM,SLM ( we are not using CFM on ELAN service's on NCS)
	+ HQOS uses Igress marking + Parent & child Rate limiting Policy  ( 5 Class)
	+ FLAT QOS uses Egress Marking Policy QOS_NNI_egress.
	+ Flat QOS uses Egress Shaping Policy.
+ Create 50 Xconnect Services with FLAT QOS and CCM
	+ Flat QOS uses Igress marking + Rate limiting Policy 
	+ FLAT QOS uses Egress Marking Policy QOS_NNI_egress.
	+ Flat QOS uses Egress Shaping Policy ( Parent + child)
	+ CCM is Enabled.
+ Create 100 Xconnect services with FLAT QOS, CCM, DM,SL.
	+ Flat QOS has earlier Attributes.
    + CCM is enabled.
	+ DM & SLM is enabled.
+ Check the no of ELAN and XC services.
+ Delete ELAN services.
+ Delete X connect Services.
+ Delete HQOS Policy
+ Delete FLAT QOS Policy

** intotal creates 50 ELAN and 150 Xconnect

++ ELAN Service sample Config : 
*******************************************************************************************
l2vpn bridge group AR5-AR6-AR14-DIP-FFCC-1
l2vpn bridge group AR5-AR6-AR14-DIP-FFCC-1 bridge-domain AR5-AR6-AR14-DIP-FFCC-1
l2vpn bridge group AR5-AR6-AR14-DIP-FFCC-1 bridge-domain AR5-AR6-AR14-DIP-FFCC-1 mac limit maximum 100
l2vpn bridge group AR5-AR6-AR14-DIP-FFCC-1 bridge-domain AR5-AR6-AR14-DIP-FFCC-1 mac limit action no-flood
l2vpn bridge group AR5-AR6-AR14-DIP-FFCC-1 bridge-domain AR5-AR6-AR14-DIP-FFCC-1 mtu 1500
l2vpn bridge group AR5-AR6-AR14-DIP-FFCC-1 bridge-domain AR5-AR6-AR14-DIP-FFCC-1 interface TenGigE0/0/1/3/2.1
l2vpn bridge group AR5-AR6-AR14-DIP-FFCC-1 bridge-domain AR5-AR6-AR14-DIP-FFCC-1 interface TenGigE0/0/1/3/2.1 storm-control unknown-unicast kbps 20000
l2vpn bridge group AR5-AR6-AR14-DIP-FFCC-1 bridge-domain AR5-AR6-AR14-DIP-FFCC-1 interface TenGigE0/0/1/3/2.1 storm-control multicast kbps 20000
l2vpn bridge group AR5-AR6-AR14-DIP-FFCC-1 bridge-domain AR5-AR6-AR14-DIP-FFCC-1 interface TenGigE0/0/1/3/2.1 storm-control broadcast kbps 20000
l2vpn bridge group AR5-AR6-AR14-DIP-FFCC-1 bridge-domain AR5-AR6-AR14-DIP-FFCC-1 evi 40001
interface TenGigE0/0/1/3/2.1 l2transport
 encapsulation dot1ad 1 dot1q 1
 rewrite ingress tag pop 1 symmetric
 service-policy input P2P_PARENT_HQOS_INGRESS_DIP
 service-policy output NNI-QOS-EGRESS-InnerCoS_DIP
 service-policy output P2P_PARENT_HQOS_EGGRESS_DIP account user-defined 26
!

++ Xconnect service without DM & SL Sample config :
*******************************************************************************************
ethernet cfm domain COLT-1 level 1 id null service AR5-AR6_DIP_FF_2 xconnect group AR5-AR6_DIP_FF_2 p2p AR5-AR6_DIP_FF_2 id icc-based LE 11132FF
ethernet cfm domain COLT-1 level 1 id null service AR5-AR6_DIP_FF_2 xconnect group AR5-AR6_DIP_FF_2 p2p AR5-AR6_DIP_FF_2 id icc-based LE 11132FF continuity-check interval 10s
ethernet cfm domain COLT-1 level 1 id null service AR5-AR6_DIP_FF_2 xconnect group AR5-AR6_DIP_FF_2 p2p AR5-AR6_DIP_FF_2 id icc-based LE 11132FF mep crosscheck mep-id 2
ethernet cfm domain COLT-1 level 1 id null service AR5-AR6_DIP_FF_2 xconnect group AR5-AR6_DIP_FF_2 p2p AR5-AR6_DIP_FF_2 id icc-based LE 11132FF log continuity-check errors
ethernet cfm domain COLT-1 level 1 id null service AR5-AR6_DIP_FF_2 xconnect group AR5-AR6_DIP_FF_2 p2p AR5-AR6_DIP_FF_2 id icc-based LE 11132FF log crosscheck errors
ethernet cfm domain COLT-1 level 1 id null service AR5-AR6_DIP_FF_2 xconnect group AR5-AR6_DIP_FF_2 p2p AR5-AR6_DIP_FF_2 id icc-based LE 11132FF log continuity-check mep changes
interface TenGigE0/0/1/3/2.2 l2transport ethernet cfm mep domain COLT-1 service AR5-AR6_DIP_FF_2 mep-id 1
interface TenGigE0/0/1/3/2.2 l2transport ethernet cfm mep domain COLT-1 service AR5-AR6_DIP_FF_2 mep-id 1 cos 2
l2vpn xconnect group AR5-AR6_DIP_FF_2
l2vpn xconnect group AR5-AR6_DIP_FF_2 p2p AR5-AR6_DIP_FF_2
l2vpn xconnect group AR5-AR6_DIP_FF_2 p2p AR5-AR6_DIP_FF_2 interface TenGigE0/0/1/3/2.2
l2vpn xconnect group AR5-AR6_DIP_FF_2 p2p AR5-AR6_DIP_FF_2 neighbor evpn evi 50002 target 50002 source 50002
interface TenGigE0/0/1/3/2.2 l2transport
 encapsulation dot1ad 2 dot1q 2
 rewrite ingress tag pop 1 symmetric
 ethernet cfm
  mep domain COLT-1 service AR5-AR6_DIP_FF_2 mep-id 1
   cos 2
  !
 !
 service-policy input BW-1000000Kbps-Class-B2-TG_DIP
 service-policy output NNI-QOS-EGRESS-InnerCoS_DIP
 service-policy output SHAPE-1000000Kbps-Class-B2-GE_DIP account user-defined 26
!

++ X connect with DM & SL sample config
*******************************************************************************************
ethernet cfm domain COLT-1 level 1 id null service AR5-AR6_DIP_FF_100 xconnect group AR5-AR6_DIP_FF_100 p2p AR5-AR6_DIP_FF_100 id icc-based LE 1113100FF
ethernet cfm domain COLT-1 level 1 id null service AR5-AR6_DIP_FF_100 xconnect group AR5-AR6_DIP_FF_100 p2p AR5-AR6_DIP_FF_100 id icc-based LE 1113100FF continuity-check interval 10s
ethernet cfm domain COLT-1 level 1 id null service AR5-AR6_DIP_FF_100 xconnect group AR5-AR6_DIP_FF_100 p2p AR5-AR6_DIP_FF_100 id icc-based LE 1113100FF mep crosscheck mep-id 2
ethernet cfm domain COLT-1 level 1 id null service AR5-AR6_DIP_FF_100 xconnect group AR5-AR6_DIP_FF_100 p2p AR5-AR6_DIP_FF_100 id icc-based LE 1113100FF log continuity-check errors
ethernet cfm domain COLT-1 level 1 id null service AR5-AR6_DIP_FF_100 xconnect group AR5-AR6_DIP_FF_100 p2p AR5-AR6_DIP_FF_100 id icc-based LE 1113100FF log crosscheck errors
ethernet cfm domain COLT-1 level 1 id null service AR5-AR6_DIP_FF_100 xconnect group AR5-AR6_DIP_FF_100 p2p AR5-AR6_DIP_FF_100 id icc-based LE 1113100FF log continuity-check mep changes
interface TenGigE0/0/1/3/2.100 l2transport ethernet cfm mep domain COLT-1 service AR5-AR6_DIP_FF_100 mep-id 1
interface TenGigE0/0/1/3/2.100 l2transport ethernet cfm mep domain COLT-1 service AR5-AR6_DIP_FF_100 mep-id 1 cos 2
interface TenGigE0/0/1/3/2.100 l2transport ethernet cfm mep domain COLT-1 service AR5-AR6_DIP_FF_100 mep-id 1 sla operation profile DMM2 target mep-id 2
interface TenGigE0/0/1/3/2.100 l2transport ethernet cfm mep domain COLT-1 service AR5-AR6_DIP_FF_100 mep-id 1 sla operation profile SLM2 target mep-id 2
l2vpn xconnect group AR5-AR6_DIP_FF_100
l2vpn xconnect group AR5-AR6_DIP_FF_100 p2p AR5-AR6_DIP_FF_100
l2vpn xconnect group AR5-AR6_DIP_FF_100 p2p AR5-AR6_DIP_FF_100 interface TenGigE0/0/1/3/2.100
l2vpn xconnect group AR5-AR6_DIP_FF_100 p2p AR5-AR6_DIP_FF_100 neighbor evpn evi 50100 target 50100 source 50100
 encapsulation dot1ad 100 dot1q 100
 rewrite ingress tag pop 1 symmetric
 ethernet cfm
  mep domain COLT-1 service AR5-AR6_DIP_FF_100 mep-id 1
   cos 2
   sla operation profile DMM2 target mep-id 2
   sla operation profile SLM2 target mep-id 2
  !
 !
 service-policy input BW-1000000Kbps-Class-B2-TG_DIP
 service-policy output NNI-QOS-EGRESS-InnerCoS_DIP
 service-policy output SHAPE-1000000Kbps-Class-B2-GE_DIP account user-defined 26
!

"

ansible-playbook xconnect_scale.yml --tags verify_service

ansible-playbook xconnect_scale.yml -e '{"FF_start_evi_ID":1,"FF_end_evi_ID":50,"H_QOS":"YES","Flat_QOS":"NO","CCM_REQUIRED":"n"}' --tags create_ELAN_service
ansible-playbook xconnect_scale.yml -e '{"FF_start_evi_ID":50,"FF_end_evi_ID":100,"Flat_QOS":"YES","CCM_REQUIRED":"y"}' --tags create_xc_service
a=100
b=200
 until [ $a -ge 200 ]
 do
 ansible-playbook xconnect_scale.yml -e '{"FF_start_evi_ID":'$a',"FF_end_evi_ID":'$b',"Flat_QOS":"YES","CCM_REQUIRED":"y","DM_SL_REQUIRED":"YES"}' --tags create_xc_service
 a=`expr $a + 100`
 b=`expr $b + 100` 
 done


ansible-playbook xconnect_scale.yml --tags verify_service

ansible-playbook xconnect_scale.yml -e '{"FF_start_evi_ID":1,"FF_end_evi_ID":50,"H_QOS":"YES","Flat_QOS":"NO","CCM_REQUIRED":"n"}' --tags delete_ELAN_service
ansible-playbook xconnect_scale.yml -e '{"FF_start_evi_ID":50,"FF_end_evi_ID":100,"Flat_QOS":"YES","CCM_REQUIRED":"y"}' --tags delete_xc_service
a=100
b=200
 until [ $a -ge 200 ]
 do
 ansible-playbook xconnect_scale.yml -e '{"FF_start_evi_ID":'$a',"FF_end_evi_ID":'$b',"QOS_REQUIRED":'YES',"Flat_QOS":"YES","CCM_REQUIRED":"y","DM_SL_REQUIRED":"YES"}' --tags delete_xc_service
 a=`expr $a + 100`
 b=`expr $b + 100` 
 done

ansible-playbook xconnect_scale.yml -e '{"FF_start_evi_ID":1,"FF_end_evi_ID":2}' --tags delete_policy