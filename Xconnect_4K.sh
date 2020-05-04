#!/bin/sh
echo "
************
Test 4K Xconnect per device.
***********
"

ansible-playbook xconnect_scale.yml --tags verify_service

a=1
b=200
 until [ $a -ge 4000 ]
 do
 ansible-playbook xconnect_scale.yml -e '{"FF_start_evi_ID":'$a',"FF_end_evi_ID":'$b',"Flat_QOS":"NO","CCM_REQUIRED":"n","DM_SL_REQUIRED":"NO"}' --tags create_xc_service
 a=`expr $a + 199`
 b=`expr $b + 200` 
 done

ansible-playbook xconnect_scale.yml --tags verify_service

a=1
b=200
 until [ $a -ge 4000 ]
 do
 ansible-playbook xconnect_scale.yml -e '{"FF_start_evi_ID":'$a',"FF_end_evi_ID":'$b',"Flat_QOS":"NO","CCM_REQUIRED":"n","DM_SL_REQUIRED":"NO"}' --tags delete_xc_service
 a=`expr $a + 199`
 b=`expr $b + 200` 
 done

ansible-playbook xconnect_scale.yml -e '{"FF_start_evi_ID":1,"FF_end_evi_ID":2}' --tags delete_policy