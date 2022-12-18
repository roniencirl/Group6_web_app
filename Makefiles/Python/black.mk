# pinning to a known version of black.
BLACK_EXE := docker run --rm \
	-v $(shell pwd):/data \
	-w=/data \
	cytopia/black@sha256:a477841f7262f1eacb440b0199503d97f0f779ef1a5d270599c2a1fe8b6f4bc1 \
	 -v .

.PHONY: create_pytoml
create_pytoml: 
	# start at tool.black, stop at newline immediately followed by [ (start of section header)
	${SED_EXE} -n '/\[tool.black\]/,/^$[/p' setup.cfg > pyproject.toml

.PHONY: remove_pytoml
remove_pytoml:
	cat $(REPO_DIR)/pyproject.toml
	rm $(REPO_DIR)/pyproject.toml

.PHONY: black_format
black_format: ## Format python files with black.
	if [ ! -f $(REPO_DIR)/pyproject.toml ]; then make create_pytoml; fi
	$(BLACK_EXE)

.PHONY: black_check
black_check: ## Run black formatting check.
	@echo "-------------------- Black Lint --------------------"
	if [ ! -f $(REPO_DIR)/pyproject.toml ]; then make create_pytoml; fi
	$(BLACK_EXE) --check
