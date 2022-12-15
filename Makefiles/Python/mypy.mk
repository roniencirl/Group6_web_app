MYPY_EXE := docker run --rm \
		-v $(shell pwd):/data \
		-w=/data \
		cytopia/mypy\
			.

.PHONY: create_mypy_ini
create_mypy_ini:
	${SED_EXE} -n '/\[mypy\]/,/^\s*$$/p' setup.cfg > mypy.ini

.PHONY: remove_mypy_ini
remove_mypy_ini:
	rm -f $(shell pwd)/mypy.ini

.PHONY: mypy_check
mypy_check: mypy_check
	@echo "-------------------- MYPY Check --------------------"
	if [ ! -f $(REPO_DIR)/pyproject.toml ]; then make create_mypy_ini; fi
	${MYPY_EXE}
	make remove_mypy_ini

