#!/bin/sh
echo "
************
Multi-Dimension test Case
***********
"
step=50

ansible-playbook xconnect_scale.yml --tags verify_service
ansible-playbook xconnect_scale.yml -e '{"FF_start_evi_ID":1,"FF_end_evi_ID":2}' --tags configure_policy
ansible-playbook xconnect_scale.yml -e '{"FF_start_evi_ID":1,"FF_end_evi_ID":50,"H_QOS":"YES","Flat_QOS":"NO","CCM_REQUIRED":"n"}' --tags create_ELAN_service
ansible-playbook xconnect_scale.yml -e '{"FF_start_evi_ID":50,"FF_end_evi_ID":100,"Flat_QOS":"YES","CCM_REQUIRED":"y","DM_SL_REQUIRED":"YES"}' --tags create_xc_service
a=100
b=150
 until [ $a -ge 400 ]
 do
 ansible-playbook xconnect_scale.yml -e '{"FF_start_evi_ID":'$a',"FF_end_evi_ID":'$b',"Flat_QOS":"YES","CCM_REQUIRED":"y"}' --tags create_xc_service
 a=`expr $a + $step`
 b=`expr $b + $step` 
 done

a=500
b=550
 until [ $a -ge 900 ]
 do
 ansible-playbook xconnect_scale.yml -e '{"FF_start_evi_ID":'$a',"FF_end_evi_ID":'$b',"Flat_QOS":"YES","CCM_REQUIRED":"y"}' --tags create_xc_service_CORE1
 a=`expr $a + $step`
 b=`expr $b + $step` 
 done

ansible-playbook xconnect_scale.yml --tags verify_service
ansible-playbook verifier.yml -e '{"FF_start_evi_ID":50,"FF_end_evi_ID":400}'
ansible-playbook verifier.yml -e '{"FF_start_evi_ID":500,"FF_end_evi_ID":900}'

ls -lrt
chmod 777 spirent_traffic/
ls -lrt
cd spirent_traffic/
ls -lrt
python service_traffic_400.py
ls -lrt
cd ..
ls -lrt

ansible-playbook xconnect_scale.yml -e '{"FF_start_evi_ID":1,"FF_end_evi_ID":50,"H_QOS":"YES","Flat_QOS":"NO","CCM_REQUIRED":"n"}' --tags delete_ELAN_service
ansible-playbook xconnect_scale.yml -e '{"FF_start_evi_ID":50,"FF_end_evi_ID":100,"Flat_QOS":"YES","CCM_REQUIRED":"y"}' --tags delete_xc_service
a=100
b=150
 until [ $a -ge 400 ]
 do
 ansible-playbook xconnect_scale.yml -e '{"FF_start_evi_ID":'$a',"FF_end_evi_ID":'$b',"QOS_REQUIRED":'YES',"Flat_QOS":"YES","CCM_REQUIRED":"y"}' --tags delete_xc_service
 a=`expr $a + $step`
 b=`expr $b + $step` 
 done

a=500
b=550
 until [ $a -ge 900 ]
 do
 ansible-playbook xconnect_scale.yml -e '{"FF_start_evi_ID":'$a',"FF_end_evi_ID":'$b',"QOS_REQUIRED":'YES',"Flat_QOS":"YES","CCM_REQUIRED":"y"}' --tags delete_xc_service_CORE1
 a=`expr $a + $step`
 b=`expr $b + $step` 
 done