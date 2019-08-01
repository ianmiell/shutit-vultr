import os
import shutit
import sys

try:
	api_key = os.environ['VULTR_API_KEY']
except:
	print('VULTR_API_KEY must be set in the environment')
	sys.exit(1)

s = shutit.create_session(docker_image='ubuntu:19.04', docker_rm=True, loglevel='INFO', session_type='docker')
s.send('TODO install terraform, add provider')
s.send('TODO install golang')
s.install('git')
s.send('git clone https://terraform scripts')
s.send('cd terraform scripts')
s.send('terraform init')
s.send('terraform apply')

TODO: get the ip address and login - ask user to input? can it be included in the terraform script?


