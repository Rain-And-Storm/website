#!/usr/bin/make -f

# Makefile for website generator

BUILD_DIR = docs
CONFIG_FILE = config.ini
DOCKER ?= $(if $(shell docker -v),docker,podman)
DOCKER_IMAGE_TAG ?= svcuriouscat-website-generator

all: build

build: clean $(BUILD_DIR) $(CONFIG_FILE)
	@cd $(BUILD_DIR) && \
	python3 ../website-generator.py
.PHONY: build

build-using-docker: clean $(BUILD_DIR) $(CONFIG_FILE)
	@$(DOCKER) build -t $(DOCKER_IMAGE_TAG) .
	@$(DOCKER) run --rm $(DOCKER_IMAGE_TAG) sh -c "tar -c -f docs.tar docs && cat docs.tar" | tar -x -f -
.PHONY: build-using-docker

$(CONFIG_FILE):
	@cp -n config.def.ini $(CONFIG_FILE)

clean:
	@if [ -d $(BUILD_DIR) ]; then cd $(BUILD_DIR) && rm -rf {,.[!.],..?}*; fi
# 	@if [ -d $(BUILD_DIR) ]; then cd $(BUILD_DIR) && git rm -rf *; fi
.PHONY: clean

$(BUILD_DIR):
	@mkdir $(BUILD_DIR)

install-dependencies:
	@pip3 install --user -r requirements.txt
.PHONY: install-dependencies

serve: $(BUILD_DIR)
	@cd $(BUILD_DIR) && \
	echo "Starting local server at http://0.0.0.0:8100" && \
	python3 -m http.server 8100
.PHONY: serve

# TODO: serve-using-docker
