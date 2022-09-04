FROM alpine:latest

RUN apk update && apk add gcc g++ make musl-dev python3 python3-dev py3-pip py3-wheel

WORKDIR /src/website-generator

ADD Makefile requirements.txt .

RUN make INSTALL_DEPS

ADD . .

RUN make BUILD
