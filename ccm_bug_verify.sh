ansible-playbook xconnect_scale.yml -e '{"FF_start_evi_ID":50,"FF_end_evi_ID":100,"Flat_QOS":"YES","CCM_REQUIRED":"y","DM_SL_REQUIRED":"YES"}' --tags create_xc_service
ansible-playbook verifier.yml -e '{"FF_start_evi_ID":50,"FF_end_evi_ID":99}'

ansible-playbook xconnect_scale.yml -e '{"FF_start_evi_ID":100,"FF_end_evi_ID":200,"Flat_QOS":"YES","CCM_REQUIRED":"y"}' --tags create_xc_service
ansible-playbook verifier.yml -e '{"FF_start_evi_ID":50,"FF_end_evi_ID":199}'

ansible-playbook xconnect_scale.yml -e '{"FF_start_evi_ID":200,"FF_end_evi_ID":300,"Flat_QOS":"YES","CCM_REQUIRED":"y"}' --tags create_xc_service
ansible-playbook verifier.yml -e '{"FF_start_evi_ID":50,"FF_end_evi_ID":299}'


ansible-playbook xconnect_scale.yml -e '{"FF_start_evi_ID":300,"FF_end_evi_ID":400,"Flat_QOS":"YES","CCM_REQUIRED":"y"}' --tags create_xc_service
ansible-playbook verifier.yml -e '{"FF_start_evi_ID":50,"FF_end_evi_ID":399}'

ansible-playbook xconnect_scale.yml -e '{"FF_start_evi_ID":500,"FF_end_evi_ID":600,"Flat_QOS":"YES","CCM_REQUIRED":"y"}' --tags create_xc_service_CORE1
ansible-playbook verifier.yml -e '{"FF_start_evi_ID":50,"FF_end_evi_ID":399}'
ansible-playbook verifier.yml -e '{"FF_start_evi_ID":500,"FF_end_evi_ID":599}'


ansible-playbook xconnect_scale.yml -e '{"FF_start_evi_ID":600,"FF_end_evi_ID":700,"Flat_QOS":"YES","CCM_REQUIRED":"y"}' --tags create_xc_service_CORE1
ansible-playbook verifier.yml -e '{"FF_start_evi_ID":50,"FF_end_evi_ID":399}'
ansible-playbook verifier.yml -e '{"FF_start_evi_ID":500,"FF_end_evi_ID":699}'