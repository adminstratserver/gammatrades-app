# pull official base image
FROM ubuntu:18.04

# set work directory
WORKDIR /usr/src/app

# set environment variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

ENV TZ=Asia/Singapore
RUN ln -snf /usr/share/zoneinfo/$TZ /etc/localtime && echo $TZ > /etc/timezone

RUN apt-get update && apt-get install -y \
    openssh-server\
    curl \
    python3-pip\
    python3-dev \
    libpq-dev \
    postgresql \
    postgresql-contrib \
    git

RUN pip3 install \
        django==3.0.7 \
        Pillow==7.2.0 \
        djangorestframework==3.10.3 \
        django-rest-auth==0.9.5 \
        python-dotenv==0.13.0 \
        django-cors-headers==3.4.0 \
        django-allauth==0.42.0 \
        asgiref==3.2.3 \
        psycopg2==2.8.3 \
        psycopg2-binary==2.8.3 \
        gunicorn==19.7.1 \
        django-storages==1.9.1 \
        boto3==1.14.11

# run entrypoint.sh
ENTRYPOINT ["/usr/src/app/entrypoint.prod.sh"]

RUN adduser remote_user && \
    echo remote_user:1234 | chpasswd && \
    mkdir /home/remote_user/.ssh && \
    chmod 700 /home/remote_user/.ssh

RUN echo 'ssh-rsa AAAAB3NzaC1yc2EAAAADAQABAAABAQDAbMEL2d3vdprIcHWM6CW+b89lisiHY5a3Yl/IS8I8+8fMQwxkkA0+Xeu9BI2orl92+nF7swfUFelc5d3xmvDVDD9YAda5CWSb0ogpFsqhSs96faHZYDbxaP8zjclkgpyuJAuqLK8oGdnuqesip2rTd7tiCTGzynPieTTnUKmoW3A7LhfrjpEyouxixcKzYJhPwb+1ciUzOnV+eKlPlGaVuaBPesAa8ABpOO7XihAzmMY+OzsNxtDhcNOscZtBrfznLRsr5jNbOtsVnllXFG2F8QB0M5BeaXnMCKlcQaxySiNs7+aZYutWIkN6GVmGa7mOX7+PAC1DMspPd/hhFW09 root@localhost' \
      > /home/remote_user/.ssh/authorized_keys

# COPY ./remote-key.pub /home/remote_user/.ssh/authorized_keys
RUN chown remote_user:remote_user -R /home/remote_user/.ssh && \
    chmod 600 /home/remote_user/.ssh/authorized_keys



RUN mkdir /var/run/sshd
RUN echo 'root:THEPASSWORDYOUCREATED' | chpasswd
RUN sed -i 's/PermitRootLogin prohibit-password/PermitRootLogin yes/' /etc/ssh/sshd_config

# SSH login fix. Otherwise user is kicked off after login
RUN sed 's@session\s*required\s*pam_loginuid.so@session optional pam_loginuid.so@g' -i /etc/pam.d/sshd

ENV NOTVISIBLE "in users profile"
RUN echo "export VISIBLE=now" >> /etc/profile

EXPOSE 22
CMD ["/usr/sbin/sshd", "-D"]
