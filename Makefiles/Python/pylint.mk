# set options in setup.cfg in project root
# set PYLINT_MODULES in Makefile
# PYLINT_MODULES="./src/module1 ./src/module2"
.PHONY: pylint_check
pylint_check: ## Run pylint check.
	@echo "-------------------- PYLINT --------------------"
	docker run --rm \
		-v $(shell pwd):/data \
		-w=/data \
		cytopia/pylint \
			$(PYLINT_MODULES)
