import os
import shutit
import sys
import pick

## BEGIN CORE SETUP
def core_setup(s, vultr_password, api_key):
	if s.command_available('docker'):
		s.login(command='docker run -ti imiell/vultr-bare-metal bash')
	elif s.command_available('podman'):
		s.login(command='podman run -ti imiell/vultr-bare-metal bash')
	elif s.command_available('buildah'):
		s.login(command='buildah -ti imiell/vultr-bare-metal bash')
	else:
		s.handle_exit(exit_code=1,msg='No command found to run image')
	# regions baremetal is available: https://www.vultr.com/api/#plans_plan_list_baremetal
	available_region = s.send_and_get_output('''curl -s https://api.vultr.com/v1/plans/list_baremetal | jq '.["100"]["available_locations"][]' | head -1''')
	s.send('export TF_VAR_token=' + api_key)
	s.send('cd vultr-bare-metal')
	s.send('git pull')
	ip_address = s.send_and_get_output("terraform apply -auto-approve -no-color -var 'vultr_bm_region=" + available_region + "' | grep '^ip' | awk '{print $3}'")
	s.send('sleep 120')
	s.login(command='ssh root@' + ip_address, password=vultr_password)
	s.send('apt-get upgrade -y')
	s.send('apt-get install -y python-pip build-essential virtualbox tmux vim')
	s.send('apt-get autoremove -y')
	s.send('pip install setuptools')
	s.send('pip install wheel')
	s.send('pip install shutit pygithub')
	s.send('''echo 'export PATH=$PATH:/root/bin' >> /root/.bashrc''')
	return ip_address
## END CORE SETUP

## BEGIN INSTALLS
def install_knative(s, ip_address, vultr_password):
	s.send('cd /root/shutit-minikube/')
	s.send('./run.sh knative')

def install_minikube(s):
	s.send('cd /root')
	s.send('curl -Lo minikube https://storage.googleapis.com/minikube/releases/latest/minikube-linux-amd64 && chmod +x minikube && mv minikube /usr/local/bin')
	s.send('git clone https://github.com/ianmiell/shutit-minikube')
	s.send('''(cd shutit-minikube && touch secret && git submodule init && git submodule update)''')

def install_minishift(s):
	s.send('cd /root')
	# TODO download minishift
	s.send('git clone https://github.com/ianmiell/shutit-minishift')
	s.send('''(cd shutit-minishift && touch secret && git submodule init && git submodule update)''')


def install_kubebuilder(s):
	# https://book.kubebuilder.io/quick-start.html#installation
	s.send('cd /root')
	s.send('curl -sL https://go.kubebuilder.io/dl/2.0.0-beta.0/${os}/${arch} | tar -xz -C /tmp/')
	s.send('mv /tmp/kubebuilder_2.0.0-beta.0_${os}_${arch} /usr/local/kubebuilder')
	s.send('export PATH=$PATH:/usr/local/kubebuilder/bin')
	s.send('''echo 'export PATH=$PATH:/usr/local/kubebuilder/bin' >> /root/.bashrc''')

def install_kustomize(s):
	# https://github.com/kubernetes-sigs/kustomize/blob/master/docs/INSTALL.md
	s.send('cd /root')
	s.send('opsys=linux')  # or darwin, or windows
	s.send('''curl -s https://api.github.com/repos/kubernetes-sigs/kustomize/releases/latest | grep browser_download | grep $opsys |cut -d '"' -f 4 | xargs curl -O -L''')
	s.send('mv kustomize_*_${opsys}_amd64 /usr/bin/local/kustomize')
	s.send('chmod u+x /usr/bin/local/kustomize')

def install_go(s):
	s.send('cd /root')
	s.send('wget https://dl.google.com/go/go1.12.7.linux-amd64.tar.gz')
	s.send('tar -xvf go1.12.7.linux-amd64.tar.gz')
	s.send('rm -f go1.12.7.linux-amd64.tar.gz')
	s.send('export PATH=${PATH}:/root/go/bin')
	s.send('''echo 'export PATH=${PATH}:/root/go/bin' >> /root/.bashrc''')

def install_kn(s):
	install_go(s)
	s.send('go get https://github.com/knative/client')

def install_ko(s):
	install_go(s)
	s.send('go get github.com/google/go-containerregistry/cmd/ko')

def install_knctl(s):
#https://github.com/cppforlife/knctl
	s.send('cd /root')
	s.send('git clone https://github.com/cppforlife/knctl')
	s.send('cd knctl')
	s.send('./hack/build.sh')
## INSTALLS DONE

## BEGIN ACTIVITIES
def do_knative_serving_example(s):
	## Hello world: https://koudingspawn.de/knative-serving/
	## Minio client
	s.send('cd /root')
	s.send('wget https://dl.min.io/client/mc/release/linux-amd64/mc && chmod +x mc && mv mc /usr/local/bin/mc')
	s.send('git clone https://gitlab.com/koudingspawn-public/knative/simple-serving-hello')
	s.send('cd simple-serving-hello')
	s.send('#kubectl apply -f kubernetes/serving.yaml')
	s.send_until('kubectl get ksvc -n simple-serving | grep  http://simple-serving-java.simple-serving.example.com | grep True | wc -l', '1')
	s.send('kubectl apply -f kubernetes/allow-minio.yaml')
	s.send('kubectl apply -f minio/deployment.yaml')
	minio_podname = s.send("kubectl get pods -n minio | grep minio | awk '{print $1}'")
	s.send('kubectl port-forward -n minio pod/' + MINIO_PODNAME + '9000:9000 &')
	s.send('mc config host add minio http://120.0.0.1:9000 minio minio123')
	s.send('mc mb minio/images')
	s.send('mc mb minio/thumbnail')
	s.send('mc event add minio/images arn:minio:sqs::1:webhook --event put --suffix .jpg')
## ACTIVITIES DONE

## HANDLERS BEGIN
def handle_knative(s, ip_address, vultr_password):
	setup_minikube(s)
	install_knative(s=s, ip_address=ip_address, vultr_password=vultr_password)
	final_msg += 'knative set up and ready to use at: ' + ip_address + ', with root password: ' + vultr_password
	q = 'Please choose an activity to perform'
	knative_options = ['knative_serving_example',]
	knative_option, _ = pick.pick(knative_options, q)
	if knative_option == 'knative_serving_example':
		do_knative_serving_example(s)
	s.pause_point(final_msg)
## HANDLERS DONE

## MAIN BEGIN
def main():
	# Pre-req check
	try:
		api_key = os.environ['VULTR_API_KEY']
	except:
		print('VULTR_API_KEY must be set in the environment')
		sys.exit(1)
	# Constants
	vultr_password = 'vultr0987'
	# Main choices begin
	q = 'Please choose an env to build'
	env_options = ['knative',]
	env_option, _ = pick.pick(env_options, q)
	final_msg = ''

	# Create bash shell
	s = shutit.create_session(loglevel='DEBUG', session_type='bash', echo=True)
	ip_address = core_setup(s=s, vultr_password=vultr_password, api_key=api_key)

	# Process choices
	if env_option == 'knative':
		handle_knative(s, ip_address, vultr_password)

	# Clean up from core setup.
	s.logout()
	s.logout()
## MAIN DONE

main()
