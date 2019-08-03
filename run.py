import os
import shutit
import sys

try:
	api_key = os.environ['VULTR_API_KEY']
except:
	print('VULTR_API_KEY must be set in the environment')
	sys.exit(1)

s = shutit.create_session(loglevel='DEBUG', session_type='bash')
s.login('docker run -ti imiell/vultr-bare-metal bash')
# regions baremetal is available: https://www.vultr.com/api/#plans_plan_list_baremetal
available_region = s.send_and_get_output('''curl -q https://api.vultr.com/v1/plans/list_baremetal | jq '.["100"]["available_locations"][]' | head -1''')
s.send('export TF_VAR_token=' + api_key)
s.send('cd vultr-bare-metal')
s.send('git pull')
output = s.send_and_get_output("terraform apply -auto-approve -no-color -var 'vultr_bm_region=" + available_region + "'")
s.pause_point('')
# TODO extract IP address from output
#ip_address =
#s.login(command='ssh root@' + ip_address, password='vultr')
# TODO: run up knative
