#!/bin/sh
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

# ansible-playbook xconnect_scale.yml -e '{"FF_start_evi_ID":1,"FF_end_evi_ID":50,"H_QOS":"YES","Flat_QOS":"NO","CCM_REQUIRED":"y"}' --tags delete_ELAN_service
# ansible-playbook xconnect_scale.yml -e '{"FF_start_evi_ID":50,"FF_end_evi_ID":100,"Flat_QOS":"YES","CCM_REQUIRED":"y"}' --tags delete_xc_service
# a=100
# b=200
#  until [ $a -ge 200 ]
#  do
#  ansible-playbook xconnect_scale.yml -e '{"FF_start_evi_ID":'$a',"FF_end_evi_ID":'$b',"QOS_REQUIRED":'YES',"Flat_QOS":"YES","CCM_REQUIRED":"y","DM_SL_REQUIRED":"YES"}' --tags delete_xc_service
#  a=`expr $a + 100`
#  b=`expr $b + 100` 
#  done



# ansible-playbook xconnect_scale.yml -e '{"FF_start_evi_ID":1,"FF_end_evi_ID":2}' --tags delete_policy
# ansible-playbook xconnect_scale.yml -e '{"FF_start_evi_ID":1,"FF_end_evi_ID":2,"H_QOS":"YES","Flat_QOS":"NO"}' --tags delete_policy