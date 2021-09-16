FROM nginx:latest as development_build

RUN rm /etc/nginx/conf.d/default.conf
COPY ./config/nginx/conf.d/dev.conf /etc/nginx/conf.d