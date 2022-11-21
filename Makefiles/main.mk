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

