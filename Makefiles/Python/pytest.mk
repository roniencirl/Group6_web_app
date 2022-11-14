# set options in setup.cfg in project root
.PHONY: pytes%
pytes%:
	@echo "-------------------- PYTest --------------------"
	docker run -it \
		-v $(shell pwd):/data \
		-w=/data \
		${image} \
			pytest
