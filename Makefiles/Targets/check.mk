.PHONY: python_check
python_check:
ifeq ($(strip $(shell find . -type f -name "*.py" -not -path "./.Makefiles/*")),)
	echo "Did not find any .py files. Skipping Node check"
else
	@echo "################## Running Python Check Stage ##################"
	make -f $(MAKEFILE) black_check
	make -f $(MAKEFILE) pylint_check
	make -f $(MAKEFILE) mypy_check
endif

.PHONY: python_check_format
python_check_format:
ifeq ($(strip $(shell find . -type f -name "*.py" -not -path "./.Makefiles/*")),)
	echo "Did not find any .py files. Skipping Node check"
else
	make -f $(MAKEFILE) black_format
endif

.PHONY: node_check
node_check:
ifeq ($(strip $(shell find . -type f -name "package.json" -not -path "./.Makefiles/*")),)
	@echo "Did not find any package.json files. Skipping Node check"
else
	@echo "################## Running Node Check Stage ##################"
	make -f $(MAKEFILE) standard_js_check
endif

.PHONY: node_format
node_format:
ifeq ($(strip $(shell find . -type f -name "package.json" -not -path "./.Makefiles/*")),)
	@echo "Did not find any package.json files. Skipping Node check"
else
	@echo "################## Running Node Check Format Stage ##################"
	make -f $(MAKEFILE) standard_js_format
endif

.PHONY: js_frontend_check
js_frontend_check:
ifeq ($(strip $(shell find . -type f -name ".ember-cli-build.js" -not -path "./.Makefiles/*")),)
	@echo "Did not find any .ember-cli-build.js files. Skipping JS Frontend check"
else
	@echo "################## Running JS Fontend Check Stage ##################"
	make -f $(MAKEFILE) frontend_lint_check
endif

.PHONY: go_check
go_check:
ifeq ($(strip $(shell find . -type f -name "go.mod" -not -path "./.Makefiles/*")),)
	@echo "Did not find any go.mod files. Skipping Go check"
else
	@echo "################## Running GO Check Stage ##################"
	make -f $(MAKEFILE) go_lint_check
endif

.PHONY: groovy_check
groovy_check:
ifeq ($(strip $(shell find . -type f -name "*.groovy" -not -path "./.Makefiles/*")),)
	@echo "Did not find any .groovy files. Skipping Groovy check"
else
	@echo "################## Running Groovy Check Stage ##################"
	make -f $(MAKEFILE) groovy_lint_check
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
