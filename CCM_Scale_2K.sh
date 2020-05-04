#!/bin/sh
echo "
************
Single dimension Scale for CCM 2K.
***********
"
# ansible-playbook xconnect_scale.yml --tags verify_service

# a=1
# b=200
#  until [ $a -ge 200 ]
#  do
#  ansible-playbook xconnect_scale.yml -e '{"FF_start_evi_ID":'$a',"FF_end_evi_ID":'$b',"QOS_REQUIRED":"NO","Flat_QOS":"NO","CCM_REQUIRED":"y","DM_SL_REQUIRED":"NO"}' --tags create_xc_service
#  a=`expr $a + 199`
#  b=`expr $b + 200` 
#  done

# ansible-playbook xconnect_scale.yml --tags verify_service

a=1
b=200
 until [ $a -ge 200 ]
 do
 ansible-playbook xconnect_scale.yml -e '{"FF_start_evi_ID":'$a',"FF_end_evi_ID":'$b',"QOS_REQUIRED":"NO","Flat_QOS":"NO","CCM_REQUIRED":"y","DM_SL_REQUIRED":"NO"}' --tags delete_xc_service
 a=`expr $a + 199`
 b=`expr $b + 200` 
 done