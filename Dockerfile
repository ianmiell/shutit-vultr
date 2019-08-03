FROM ubuntu:19.04
WORKDIR /root
RUN apt-get update -y && apt-get install -y unzip build-essential git wget
RUN wget https://releases.hashicorp.com/terraform/0.12.6/terraform_0.12.6_linux_amd64.zip
RUN unzip terraform_0.12.6_linux_amd64.zip
RUN mv terraform /usr/local/bin
RUN wget https://dl.google.com/go/go1.12.7.linux-amd64.tar.gz
# Install GO
RUN tar -xvf go1.12.7.linux-amd64.tar.gz
RUN mv go /usr/local
ENV GOROOT=/usr/local/go
ENV PATH=${PATH}:/usr/local/go/bin
# Install vultr provider
RUN git clone https://github.com/vultr/terraform-provider-vultr
WORKDIR /root/terraform-provider-vultr
RUN mkdir -p /usr/local/go/src/github.com/vultr
WORKDIR /usr/local/go/src/github.com/vultr
RUN git clone https://github.com/vultr/terraform-provider-vultr
WORKDIR /usr/local/go/src/github.com/vultr/terraform-provider-vultr
RUN make build && rm -rf /usr/local/go/bin/pkg/mod/cache
#RUN ln -s /usr/local/go/bin/terraform-provider-vultr ~/.terraform.d/plugins/terraform-provider-vultr
WORKDIR /root
RUN git clone https://github.com/ianmiell/vultr-bare-metal
WORKDIR /root/vultr-bare-metal
RUN terraform init -plugin-dir /root/go/bin
CMD bash
