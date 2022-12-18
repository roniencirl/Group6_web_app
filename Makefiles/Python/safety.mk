# set options in setup.cfg in project root
.PHONY: safety_check
safety_check: ## Run safety dependency security check
	@echo "-------------------- Pyup.io Safety --------------------"
	python3 -m pip freeze | tee /dev/tty | docker run -i --rm \
		-v $(shell pwd):/data \
		-w=/data \
			pyupio/safety \
			safety check --cache --stdin

