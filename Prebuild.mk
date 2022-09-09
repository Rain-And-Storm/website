#!/usr/bin/make -f

INSTALL_DEPS: ## Install required dependencies
	@pip3 install --user -r requirements.txt
.PHONY: INSTALL_DEPS
