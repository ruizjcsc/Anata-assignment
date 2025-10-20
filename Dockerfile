FROM ubuntu:latest

RUN apt-get update && apt-get install -y openssh-server

RUN mkdir -p /var/run/sshd

RUN mkdir -p /root/.ssh

RUN mkdir -p /app/images

COPY docker_access.pub /root/.ssh/authorized_keys

RUN chmod 600 /root/.ssh/authorized_keys

RUN chmod 700 /root/.ssh

RUN chmod 700 /app/images

RUN sed 's/#PermitRootLogin prohibit-password/PermitRootLogin yes/' /etc/ssh/sshd_config

EXPOSE 22

CMD ["/usr/sbin/sshd", "-D"]