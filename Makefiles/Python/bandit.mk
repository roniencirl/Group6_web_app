# set options in setup.cfg in project root
BANDIT_EXE :=	docker run --rm \
		-v $(shell pwd):/data \
		-w=/data \
		cytopia/bandit \
			-r . \
			-l


.PHONY: bandit_check 
bandit_check:
	@echo "-------------------- Bandit Check --------------------"
	${BANDIT_EXE}
	make remove_bandit_ini
