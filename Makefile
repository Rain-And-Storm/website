#!/usr/bin/make -f

# Makefile for website generator

BUILD_DIR ?= docs
CONFIG_FILE ?= config.ini
DOCKER ?= $(if $(shell docker -v),docker,podman)
DOCKER_IMAGE_TAG ?= svcuriouscat/website-generator
PORT ?= 8100

all: build serve

include Prebuild.mk

help: ## Show this helpful message
	@for ML in $(MAKEFILE_LIST); do \
		grep -E '^[a-zA-Z_-]+:.*?## .*$$' $$ML | sort | awk 'BEGIN {FS = ":.*?## "}; {printf "\033[36m%-30s\033[0m %s\n", $$1, $$2}'; \
	done
.PHONY: help

build: clean $(BUILD_DIR) $(CONFIG_FILE) ## Build and extract website files using container
	@$(DOCKER) build -t $(DOCKER_IMAGE_TAG) .
	@$(DOCKER) run --rm $(DOCKER_IMAGE_TAG) sh -c "tar -c -f - $(BUILD_DIR)" | tar -x -f -
.PHONY: build

BUILD: clean $(BUILD_DIR) $(CONFIG_FILE) ## Build website files from filesystem
	@cd $(BUILD_DIR) && \
		python3 ../website-generator.py
.PHONY: BUILD

$(CONFIG_FILE): ## Generate config file if it doesn't already exist
	@cp -n config.def.ini $(CONFIG_FILE)

clean: ## Remove everything from build directory
	@if [ -d $(BUILD_DIR) ]; then cd $(BUILD_DIR) && rm -rf {,.[!.],..?}*; fi
.PHONY: clean

$(BUILD_DIR): ## Create empty build directory
	@mkdir -p $(BUILD_DIR)

serve: $(BUILD_DIR) ## Serve website files using container
	@$(DOCKER) run -it -v "`pwd`"/$(BUILD_DIR):/src/website-generator/$(BUILD_DIR) --rm -p $(PORT):$(PORT) $(DOCKER_IMAGE_TAG)
.PHONY: serve

SERVE: $(BUILD_DIR) ## Serve website files directly from filesystem
	@cd $(BUILD_DIR) && \
		echo "Starting local server for contents of $(BUILD_DIR) ..." && \
		python3 -m http.server $(PORT)
.PHONY: SERVE
