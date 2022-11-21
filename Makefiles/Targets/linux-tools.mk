SED_EXE := docker run --rm \
	-v $(shell pwd):/data \
	-w=/data \
	hairyhenderson/sed
