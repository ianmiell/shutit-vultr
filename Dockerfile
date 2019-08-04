FROM ubuntu:19.04
WORKDIR /root
ENV PATH=${PATH}:/root/go/bin
RUN apt-get update -y && \
	apt-get install -y unzip build-essential git wget jq curl && \
	wget https://releases.hashicorp.com/terraform/0.12.6/terraform_0.12.6_linux_amd64.zip && \
    unzip terraform_0.12.6_linux_amd64.zip && \
	rm -f terraform_0.12.6_linux_amd64.zip && \
	mv terraform /usr/local/bin && \
	wget https://dl.google.com/go/go1.12.7.linux-amd64.tar.gz && \
	tar -xvf go1.12.7.linux-amd64.tar.gz && \
	rm -f go1.12.7.linux-amd64.tar.gz && \
	git clone https://github.com/vultr/terraform-provider-vultr && \
	mkdir -p /root/go/src/github.com/vultr && \
	cd /root/go/src/github.com/vultr && \
	git clone https://github.com/vultr/terraform-provider-vultr && \
	cd /root/go/src/github.com/vultr/terraform-provider-vultr && \
	make build && \
	rm -rf /root/go/bin/pkg/mod/cache && \
	cd /root && \
	git clone https://github.com/ianmiell/vultr-bare-metal && \
	cd /root/vultr-bare-metal && \
	terraform init -plugin-dir /root/go/bin && \
	rm -rf /root/go/pkg/ /root/go/src /root/.cache && \
	apt purge -y build-essential unzip && \
	apt autoremove -y
CMD bash
