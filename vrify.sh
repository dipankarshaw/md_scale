#!/bin/sh
# echo " ********* Check CCM status of all X-connect services on Core 0 ********* "
# ansible-playbook verifier.yml -e '{"FF_start_evi_ID":1,"FF_end_evi_ID":820}' --tags ccm_verify
# echo " ********* Check DM stats of 100 services on Core 0 ********* "
# ansible-playbook verifier.yml -e '{"FF_start_evi_ID":1,"FF_end_evi_ID":820}' --tags dmm_verifyA
# echo " ********* Check DM stats of 100 services on Core 0 ********* "
ansible-playbook verifier.yml -e '{"FF_start_evi_ID":782,"FF_end_evi_ID":784}' --tags slm_verifyA