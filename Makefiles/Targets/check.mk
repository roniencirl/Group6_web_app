.PHONY: python_check
python_check: ## Run black, pylint, mypy, bandit and safety checks
ifeq ($(strip $(shell find . -type f -name "*.py" -not -path "./Makefiles/*")),)
	echo "Did not find any .py files. Skipping Node check"
else
	@echo "################## Running Python Check Stage ##################"
	make -f $(MAKEFILE) black_check
	make -f $(MAKEFILE) pylint_check
	make -f $(MAKEFILE) mypy_check
	make -f $(MAKEFILE) bandit_check
	make -f $(MAKEFILE) safety_check
endif

.PHONY: python_check_format
python_check_format:
ifeq ($(strip $(shell find . -type f -name "*.py" -not -path "./Makefiles/*")),)
	echo "Did not find any .py files. Skipping Node check"
else
	make -f $(MAKEFILE) black_format
endif


.PHONY: docker_check
docker_check:
ifeq ($(strip $(shell find . -type f -name "*.Dockerfile" -not -path "./.Makefiles/*")),)
	@echo "Did not find any .Dockerfile files. Skipping Dockerfile check"
else
	@echo "################## Running Docker Check Stage ##################"
	make -f $(MAKEFILE) docker_lint_check
endif

.PHONY: terraform_check
terraform_check:
ifeq ($(strip $(shell find . -type f -name "*.tf" -not -path "./.Makefiles/*")),)
	@echo "Did not find any .tf files. Skipping Terraform check"
else
	@echo "################## Running Terraform Check Stage ##################"
	make -f $(MAKEFILE) terraform_lint_check
endif

.PHONY: terraform_check_format
terraform_check_format:
ifeq ($(strip $(shell find . -type f -name "*.tf" -not -path "./.Makefiles/*")),)
	@echo "Did not find any .tf files. Skipping Terraform check_format"
else
	make -f $(MAKEFILE) terraform_format
endif

.PHONY: terragrunt_check
terragrunt_check:
ifeq ($(strip $(shell find . -type f -name "*.hcl" -not -path "./.Makefiles/*")),)
	@echo "Did not find any .hcl files. Skipping Terragrunt check"
else
	@echo "################## Running Terragrunt Check Stage ##################"
	make -f $(MAKEFILE) terragrunt_lint_check
endif

.PHONY: terragrunt_check_format
terragrunt_check_format:
ifeq ($(strip $(shell find . -type f -name "*.hcl" -not -path "./.Makefiles/*")),)
	@echo "Did not find any .hcl files. Skipping Terragrunt check_format"
else
	make -f $(MAKEFILE) terragrunt_format
endif
