FROM nginx:1.15-alpine

RUN apk update
RUN apk add openssl

RUN rm -f /etc/nginx/conf.d/*
RUN mkdir /certs/
RUN mkdir /www

COPY index.html /www
COPY default.conf /etc/nginx/conf.d/default.conf
COPY nginx-selfsigned.key /etc/ssl/private/
COPY nginx-selfsigned.crt /etc/ssl/certs/
COPY dhparam.pem /etc/ssl/certs/
COPY snippets/self-signed.conf /etc/nginx/snippets/self-signed.conf
COPY snippets/ssl-params.conf /etc/nginx/snippets/ssl-params.conf