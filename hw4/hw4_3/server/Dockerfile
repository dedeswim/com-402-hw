FROM nginx:1.15-alpine

RUN apk update
RUN apk add openssl

RUN rm -f /etc/nginx/conf.d/*
RUN mkdir /certs/
RUN mkdir /www

COPY index.html /www
COPY default.conf /etc/nginx/conf.d/default.conf
COPY request.key /etc/ssl/private/request.key
COPY request.crt /etc/ssl/certs/request.crt
COPY dhparam.pem /etc/ssl/certs/