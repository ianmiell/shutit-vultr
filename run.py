import os
import shutit
import sys

try:
	api_key = os.environ['VULTR_API_KEY']
except:
	print('VULTR_API_KEY must be set in the environment')
	sys.exit(1)

s = shutit.create_session(docker_image='ubuntu:19.04', docker_rm=True, loglevel='INFO', session_type='docker')
# Install terraform
s.send('apt-get install -y unzip')
s.send('wget https://releases.hashicorp.com/terraform/0.12.6/terraform_0.12.6_linux_amd64.zip')
s.send('unzip terraform_0.12.6_linux_amd64.zip')
s.send('mv terraform /usr/local/bin')
s.send('wget https://dl.google.com/go/go1.12.7.linux-amd64.tar.gz')
# Install GO
s.send('tar -xvf go1.12.7.linux-amd64.tar.gz')
s.send('mv go /usr/local')
s.send('export GOROOT=/usr/local/go')
s.send('export GOPATH=${GOROOT}/bin')
s.send('export PATH=${PATH}:$GOPATH')
s.install('git')
# Install vultr provider
s.send('apt-get install -y build-essential')
s.send('git clone https://github.com/vultr/terraform-provider-vultr')
s.send('cd terraform-provider-vultr')
s.send('mkdir -p $GOPATH/src/github.com/vultr; cd $GOPATH/src/github.com/vultr')
s.send('git clone git@github.com:vultr/terraform-provider-vultr.git')
s.send('cd $GOPATH/src/github.com/vultr/terraform-provider-vultr')
s.send('make build')
s.send('ln -s $GOPATH/bin/terraform-provider-vultr ~/.terraform.d/plugins/terraform-provider-vultr')
s.send('git clone https://terraform scripts')
s.send('cd terraform scripts')
s.send('terraform init')
s.send('terraform apply')

TODO: get the ip address and login - ask user to input? can it be included in the terraform script? YES: https://github.com/vultr/terraform-provider-vultr/blob/master/docs/r/startup_script.html.markdown


