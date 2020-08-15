FROM nginx:1.19.1


RUN apt-get update && apt-get install -y \
    sudo \
    nano \
    systemd \
    lsof

RUN rm /etc/nginx/conf.d/default.conf
#COPY nginx.conf /etc/nginx/conf.d
