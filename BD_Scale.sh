#!/bin/sh
echo "
************
Multi-Dimension test Case
***********
"
# Configuration of services
ansible-playbook xconnect_scale.yml --tags verify_service
ansible-playbook xconnect_scale.yml -e '{"FF_start_evi_ID":1,"FF_end_evi_ID":2}' --tags configure_policy
ansible-playbook xconnect_scale.yml -e '{"FF_start_evi_ID":1,"FF_end_evi_ID":50,"H_QOS":"YES","Flat_QOS":"NO","CCM_REQUIRED":"n"}' --tags create_ELAN_service
ansible-playbook xconnect_scale.yml -e '{"FF_start_evi_ID":50,"FF_end_evi_ID":150,"Flat_QOS":"YES","CCM_REQUIRED":"y","DM_SL_REQUIRED":"YES"}' --tags create_xc_service
ansible-playbook xconnect_scale.yml -e '{"FF_start_evi_ID":150,"FF_end_evi_ID":300,"Flat_QOS":"YES","CCM_REQUIRED":"y"}' --tags create_xc_service
ansible-playbook xconnect_scale.yml -e '{"FF_start_evi_ID":300,"FF_end_evi_ID":420,"Flat_QOS":"YES","CCM_REQUIRED":"y"}' --tags create_xc_service
ansible-playbook xconnect_scale.yml -e '{"FF_start_evi_ID":500,"FF_end_evi_ID":600,"Flat_QOS":"YES","CCM_REQUIRED":"y"}' --tags create_xc_service_CORE1
ansible-playbook xconnect_scale.yml -e '{"FF_start_evi_ID":600,"FF_end_evi_ID":700,"Flat_QOS":"YES","CCM_REQUIRED":"y"}' --tags create_xc_service_CORE1
ansible-playbook xconnect_scale.yml -e '{"FF_start_evi_ID":700,"FF_end_evi_ID":800,"Flat_QOS":"YES","CCM_REQUIRED":"y"}' --tags create_xc_service_CORE1
ansible-playbook xconnect_scale.yml -e '{"FF_start_evi_ID":800,"FF_end_evi_ID":920,"Flat_QOS":"YES","CCM_REQUIRED":"y"}' --tags create_xc_service_CORE1
echo " ********* Adding a pause for 6 minutes to collect DM/SL stats ********* "
# Verification of services
sleep 6m
ansible-playbook xconnect_scale.yml --tags verify_service
ansible-playbook gather.yml
echo " ********* Check the status of all X-connect services on Core 0 ********* "
ansible-playbook verifier.yml -e '{"FF_start_evi_ID":50,"FF_end_evi_ID":420}' --tags service_verify_core0
echo " ********* Check the status of all X-connect services on Core 1 ********* "
ansible-playbook verifier.yml -e '{"FF_start_evi_ID":500,"FF_end_evi_ID":920}' --tags service_verify_core1
echo " ********* Check CCM status of all X-connect services on Core 0 ********* "
ansible-playbook verifier.yml -e '{"FF_start_evi_ID":50,"FF_end_evi_ID":420}' --tags ccm_verify
echo " ********* Check CCM status of all X-connect services on Core 1 ********* "
ansible-playbook verifier.yml -e '{"FF_start_evi_ID":500,"FF_end_evi_ID":920}' --tags ccm_verify
echo " ********* Check DM stats of 100 services on Core 0 ********* "
ansible-playbook verifier.yml -e '{"FF_start_evi_ID":50,"FF_end_evi_ID":150}' --tags dmm_verify
echo " ********* Check DM stats of 100 services on Core 0 ********* "
ansible-playbook verifier.yml -e '{"FF_start_evi_ID":50,"FF_end_evi_ID":150}' --tags slm_verify
# Spirent Traffic verification
chmod 777 spirent_traffic/
cd spirent_traffic/
python service_traffic_400.py
sleep 1m
python ELAN_RFC_Test.py
sleep 1m
python ELINE_RFC_Test.py
cd ..
#Deletion of services.
ansible-playbook xconnect_scale.yml -e '{"FF_start_evi_ID":1,"FF_end_evi_ID":50,"H_QOS":"YES","Flat_QOS":"NO","CCM_REQUIRED":"n"}' --tags delete_ELAN_service
ansible-playbook xconnect_scale.yml -e '{"FF_start_evi_ID":50,"FF_end_evi_ID":150,"Flat_QOS":"YES","CCM_REQUIRED":"y"}' --tags delete_xc_service
ansible-playbook xconnect_scale.yml -e '{"FF_start_evi_ID":150,"FF_end_evi_ID":420,"Flat_QOS":"YES","CCM_REQUIRED":"y"}' --tags delete_xc_service
ansible-playbook xconnect_scale.yml -e '{"FF_start_evi_ID":500,"FF_end_evi_ID":700,"QOS_REQUIRED":'YES',"Flat_QOS":"YES","CCM_REQUIRED":"y"}' --tags delete_xc_service_CORE1
ansible-playbook xconnect_scale.yml -e '{"FF_start_evi_ID":700,"FF_end_evi_ID":920,"QOS_REQUIRED":'YES',"Flat_QOS":"YES","CCM_REQUIRED":"y"}' --tags delete_xc_service_CORE1
