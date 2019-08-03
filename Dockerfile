FROM ubuntu:19.04
WORKDIR /root
RUN apt-get update -y && \
	apt-get install -y unzip build-essential git wget jq && \
	wget https://releases.hashicorp.com/terraform/0.12.6/terraform_0.12.6_linux_amd64.zip && \
    unzip terraform_0.12.6_linux_amd64.zip && \
	rm -f terraform_0.12.6_linux_amd64.zip && \
	mv terraform /usr/local/bin && \
	wget https://dl.google.com/go/go1.12.7.linux-amd64.tar.gz && \
	tar -xvf go1.12.7.linux-amd64.tar.gz && \
	rm -f go1.12.7.linux-amd64.tar.gz && \
	git clone https://github.com/vultr/terraform-provider-vultr && \
	mkdir -p /root/go/src/github.com/vultr
# Install vultr provider
ENV PATH=${PATH}:/root/go/bin
WORKDIR /root/go/src/github.com/vultr
RUN git clone https://github.com/vultr/terraform-provider-vultr
WORKDIR /root/go/src/github.com/vultr/terraform-provider-vultr
RUN make build && rm -rf /root/go/bin/pkg/mod/cache
WORKDIR /root
RUN git clone https://github.com/ianmiell/vultr-bare-metal
WORKDIR /root/vultr-bare-metal
RUN terraform init -plugin-dir /root/go/bin
CMD bash
