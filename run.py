import os
import shutit
import sys

try:
	api_key = os.environ['VULTR_API_KEY']
except:
	print('VULTR_API_KEY must be set in the environment')
	sys.exit(1)

s = shutit.create_session(docker_image='imiell/vultr-bare-metal', docker_rm=True, loglevel='INFO', session_type='docker')
s.send('export TF_VAR_token=' + api_key)
s.send('terraform init -plugin-dir /usr/local/go/bin')
output = s.send_and_get_output('terraform apply')
s.pause_point()
# TODO extract IP address from output
#ip_address =
#s.login(command='ssh root@' + ip_address, password='vultr')
# TODO: run up knative
