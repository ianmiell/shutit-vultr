import os
import shutit
import sys

try:
	api_key = os.environ['VULTR_API_KEY']
except:
	print('VULTR_API_KEY must be set in the environment')
	sys.exit(1)

vultr_password = 'vultr0987'

s = shutit.create_session(loglevel='INFO', session_type='bash', echo=True)
s.login(command='docker run -ti imiell/vultr-bare-metal bash')
# regions baremetal is available: https://www.vultr.com/api/#plans_plan_list_baremetal
available_region = s.send_and_get_output('''curl -s https://api.vultr.com/v1/plans/list_baremetal | jq '.["100"]["available_locations"][]' | head -1''')
s.send('export TF_VAR_token=' + api_key)
s.send('cd vultr-bare-metal')
s.send('git pull')
ip_address = s.send_and_get_output("terraform apply -auto-approve -no-color -var 'vultr_bm_region=" + available_region + "' | grep '^ip' | awk '{print $3}'")
s.send('sleep 120')
s.login(command='ssh root@' + ip_address, password=vultr_password)
s.send('git clone https://github.com/ianmiell/shutit-minishift')
s.send('git clone https://github.com/ianmiell/shutit-minikube')
s.send('''(cd shutit-minishift && touch secret && git submodule init && git submodule update)''')
s.send('''(cd shutit-minikube && touch secret && git submodule init && git submodule update)''')
s.send('apt upgrade -y')
s.send('apt install -y python-pip build-essential virtualbox tmux')
s.send('pip install setuptools')
s.send('pip install wheel')
s.send('pip install shutit pygithub')
s.send('curl -Lo minikube https://storage.googleapis.com/minikube/releases/latest/minikube-linux-amd64   && chmod +x minikube && mv minikube /usr/local/bin')
s.send('''echo 'export PATH=$PATH:/root/bin' >> /root/.bashrc''')
s.send('cd shutit-minikube/')
s.send('./run.sh knative')
s.pause_point('knative set up and ready to use at: ' + ip_address + ', with root password: ' + vultr_password)
s.logout()
s.logout()
