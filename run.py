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
s.send('export TF_VAR_token=' + api_key)
s.pause_point()
output = s.send_and_get_output('terraform apply')
# TODO extract IP address from output
#ip_address =
#s.login(command='ssh root@' + ip_address, password='vultr')
# TODO: run up knative
