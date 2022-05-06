#!/usr/bin/make -f

# Makefile for website generator

BUILD_DIR = docs
CONFIG_FILE = config.ini
SASS_OPTS = --style compressed
STYLE_FILE = $(BUILD_DIR)/_.css

all: build

build: $(BUILD_DIR) $(STYLE_FILE) $(CONFIG_FILE)
	@cd $(BUILD_DIR) && \
	python3 ../website-generator.py
.PHONY: build

$(CONFIG_FILE):
	cp -n config.def.ini $(CONFIG_FILE)

clean:
	@rm -rf $(BUILD_DIR)
.PHONY: clean

$(BUILD_DIR):
	@mkdir $(BUILD_DIR)

$(STYLE_FILE): $(BUILD_DIR)
	@which sassc > /dev/null &2> /dev/null && \
	sassc ${SASS_OPTS} src/styles/main.scss $(STYLE_FILE) || echo -n ''

serve: $(BUILD_DIR)
	@cd $(BUILD_DIR) && \
	echo "Starting local server at http://0.0.0.0:8100" && \
	python3 -m http.server 8100
.PHONY: serve

captains-log-today:
	@mkdir -p "src/data/captains-log/`date +"%Y-%m-%d"`"
.PHONY: captains-log-today

captains-log-new-record: captains-log-today
	@touch "src/data/captains-log/`date +"%Y-%m-%d"`/1-new-record.md"
.PHONY: captains-log-today-new-record
