# set options in setup.cfg in project root
.PHONY: safety_check
safety_check:
	@echo "-------------------- Pyup.io Safety --------------------"
	python3 -m pip freeze | docker run --rm \
		-v $(shell pwd):/data \
		-w=/data \
			pyupio/safety \
			safety check --cache --stdin

