# Silent output, `export VERBOSE=true` to disable
$(VERBOSE).SILENT:

# https://stackoverflow.com/questions/18136918/how-to-get-current-relative-directory-of-your-makefile
MKFILE_PATH := $(abspath $(lastword $(MAKEFILE_LIST)))
MAKEFILES_DIR := $(realpath $(notdir $(patsubst %/,%,$(dir $(MKFILE_PATH)))))
ROOT_DIR := $(patsubst %/,%,$(dir $(MAKEFILES_DIR)))
REPO_DIR :=  $(realpath $(dir $(MAKEFILES_DIR)))

# Commands
-include $(MAKEFILES_DIR)/Commands/linux-tools.mk

# Python
-include $(MAKEFILES_DIR)/Python/black.mk
-include $(MAKEFILES_DIR)/Python/mypy.mk
-include $(MAKEFILES_DIR)/Python/pylint.mk
-include $(MAKEFILES_DIR)/Python/pytest.mk
-include $(MAKEFILES_DIR)/Python/docker.mk
-include $(MAKEFILES_DIR)/Python/bandit.mk
-include $(MAKEFILES_DIR)/Python/safety.mk

# Targets 
-include $(MAKEFILES_DIR)/Targets/check.mk

# Default targets are targets with a '-default' suffix.
# To override, just redefine the target without the suffix.
# To list all available default targets: `make list-defaults`
%: %-default
	@ true

# https://www.client9.com/self-documenting-makefiles/
.PHONY=help
help: ## Display this list of annotated make targets
	@awk -F ':|##' '/^[^\t].+?:.*?##/ {\
	sub(/-default$$/, "", $$1); printf "\033[36m%-30s\033[0m %s\n", $$1, $$NF \
	}' $(MAKEFILE_LIST)

.DEFAULT_GOAL=help
