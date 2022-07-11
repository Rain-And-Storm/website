FROM alpine:latest

WORKDIR /src/website-generator

ADD Makefile .

RUN apk update && apk add make python3 py3-pip

RUN make install-dependencies

ADD . .

RUN make build
