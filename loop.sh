#!/bin/sh
ansible-playbook xconnect_scale.yml -e '{"FF_start_evi_ID":1,"FF_end_evi_ID":100,"QOS_REQUIRED":'NO', "CCM_REQUIRED":'y',"DM_SL_REQUIRED":'YES'}' --tags create_service
a=100
b=200
 until [ $a -ge 400 ]
 do
 echo " this loop configure from EVI $a to EVI $b"
 echo '!'
 echo '!'
 echo '!'
 echo '!'
 ansible-playbook xconnect_scale.yml -e '{"FF_start_evi_ID":'$a',"FF_end_evi_ID":'$b',"QOS_REQUIRED":'NO', "CCM_REQUIRED":'y'}' --tags create_service
 echo " this loop completed configuration from EVI $a to EVI $b"
 a=`expr $a + 100`
 b=`expr $b + 100` 
 done

a=400
b=500
 until [ $a -ge 800 ]
 do
 echo " this loop configure from EVI $a to EVI $b"
 echo '!'
 echo '!'
 echo '!'
 echo '!'
 ansible-playbook xconnect_scale.yml -e '{"FF_start_evi_ID":'$a',"FF_end_evi_ID":'$b',"QOS_REQUIRED":'NO'}' --tags create_service
 echo " this loop completed configuration from EVI $a to EVI $b"
 a=`expr $a + 100`
 b=`expr $b + 100` 
 done

ansible-playbook xconnect_scale.yml --tags verify_service

ansible-playbook xconnect_scale.yml -e '{"FF_start_evi_ID":1,"FF_end_evi_ID":100,"QOS_REQUIRED":'NO', "CCM_REQUIRED":'y',"DM_SL_REQUIRED":'YES'}' --tags delete_service
a=100
b=200
 until [ $a -ge 400 ]
 do
 echo " this loop delete services from EVI $a to EVI $b"
 echo '!'
 echo '!'
 echo '!'
 echo '!'
 ansible-playbook xconnect_scale.yml -e '{"FF_start_evi_ID":'$a',"FF_end_evi_ID":'$b',"QOS_REQUIRED":'NO', "CCM_REQUIRED":'y'}' --tags delete_service
 echo " this loop completed deletion of EVI $a to EVI $b"
 a=`expr $a + 100`
 b=`expr $b + 100` 
 done

a=400
b=500
 until [ $a -ge 800 ]
 do
 echo " this loop delete services from EVI $a to EVI $b"
 echo '!'
 echo '!'
 echo '!'
 echo '!'
 ansible-playbook xconnect_scale.yml -e '{"FF_start_evi_ID":'$a',"FF_end_evi_ID":'$b',"QOS_REQUIRED":'NO'}' --tags delete_service
 echo " this loop completed deletion of EVI $a to EVI $b"
 a=`expr $a + 100`
 b=`expr $b + 100` 
 done
#ansible-playbook xconnect_scale.yml -e '{"FF_start_evi_ID":1,"FF_end_evi_ID":2}' --tags delete_policy
