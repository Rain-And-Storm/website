#!/usr/bin/make -f

# Makefile for website generator

BUILD_DIR = docs
CONFIG_FILE = config.ini
DOCKER ?= $(if $(shell docker -v),docker,podman)
DOCKER_IMAGE_TAG ?= svcuriouscat/website-generator
PORT ?= 8100

all: build serve

help: ## Show this helpful message.
	@grep -E '^[a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) | sort | awk 'BEGIN {FS = ":.*?## "}; {printf "\033[36m%-30s\033[0m %s\n", $$1, $$2}'
.PHONY: help

build: CLEAN $(BUILD_DIR) $(CONFIG_FILE)
	@$(DOCKER) build -t $(DOCKER_IMAGE_TAG) .
	@$(DOCKER) run --rm $(DOCKER_IMAGE_TAG) sh -c "tar -c -f docs.tar docs && cat docs.tar" | tar -x -f -
.PHONY: build

BUILD: CLEAN $(BUILD_DIR) $(CONFIG_FILE) ## Show this helpful message.
	@cd $(BUILD_DIR) && \
	python3 ../website-generator.py
.PHONY: BUILD

$(CONFIG_FILE):
	@cp -n config.def.ini $(CONFIG_FILE)

CLEAN:
	@if [ -d $(BUILD_DIR) ]; then cd $(BUILD_DIR) && rm -rf {,.[!.],..?}*; fi
.PHONY: CLEAN

$(BUILD_DIR):
	@mkdir $(BUILD_DIR)

INSTALL_DEPS:
	@pip3 install --user -r requirements.txt
.PHONY: INSTALL_DEPS

serve:
	$(DOCKER) run -it --rm -p $(PORT):$(PORT) $(DOCKER_IMAGE_TAG)
.PHONY: serve

SERVE: $(BUILD_DIR)
	@cd $(BUILD_DIR) && \
	echo "Starting local server at http://0.0.0.0:$(PORT)" && \
	python3 -m http.server $(PORT)
.PHONY: SERVE
