FROM ubuntu:20.04

# install base packages
RUN apt update
RUN apt upgrade -y
RUN apt install -y git build-essential libpcre3 libpcre3-dev libssl-dev wget zlib1g-dev

# get nginx source and rtmp module source
WORKDIR /tmp
RUN git clone https://github.com/sergey-dryabzhinsky/nginx-rtmp-module.git
RUN wget https://nginx.org/download/nginx-1.18.0.tar.gz
RUN tar -xf nginx-1.18.0.tar.gz

# compile nginx with rtmp module
WORKDIR /tmp/nginx-1.18.0
RUN ./configure --with-http_ssl_module --add-module=../nginx-rtmp-module
RUN make -j 8
RUN make install

# setup configs
COPY nginx.conf /etc/nginx/nginx.conf
EXPOSE 1935
EXPOSE 80

# entrypoint
CMD /usr/local/nginx/sbin/nginx
