FROM openjdk:8

ENV SEATUNNEL_VERSION="2.3.3"
#COPY ./apache-seatunnel-${SEATUNNEL_VERSION}-bin.tar.gz /opt/apache-seatunnel-${SEATUNNEL_VERSION}-bin.tar.gz
COPY ./apache-seatunnel-${SEATUNNEL_VERSION}-bin-with-plugins.tar.gz /opt/apache-seatunnel-${SEATUNNEL_VERSION}-bin.tar.gz
WORKDIR /opt
RUN tar -xzvf apache-seatunnel-${SEATUNNEL_VERSION}-bin.tar.gz
RUN mv apache-seatunnel-${SEATUNNEL_VERSION} seatunnel
RUN rm -f /opt/apache-seatunnel-${SEATUNNEL_VERSION}-bin.tar.gz
WORKDIR /opt/seatunnel
ENTRYPOINT ["sh","-c"," bin/seatunnel.sh --config $config  -e local"]

# docker build -t seatunnel:2.3.3 -f Dockerfile .
# docker run   -e config="/data/seatunnel.streaming.conf" -v ./apache-seatunnel-2.3.3/config/v2.streaming.conf.template:/data/seatunnel.streaming.conf  -d  seatunnel:2.3.3
# docker logs CONTAINER ID