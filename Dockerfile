FROM ubuntu:24.04

RUN apt-get update && apt-get install -y \
make \
python3-pip

WORKDIR /src/webgen

ADD Prebuild.mk requirements.txt ./

RUN make -f Prebuild.mk INSTALL_DEPS

ADD . .

RUN make BUILD

CMD ["make", "SERVE"]
