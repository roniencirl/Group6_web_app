# set options in setup.cfg in project root
.PHONY: pytes%
pytes%:
	@echo "-------------------- pytest with coverage report--------------------"
	coverage run -m pytest .
	coverage report