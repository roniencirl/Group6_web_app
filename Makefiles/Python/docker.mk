$(eval WHO := $(shell echo $(USER) | cut -c 1-8))

PYTHON_39 := docker run --rm \
					-v "/var/run/docker.sock:/var/run/docker.sock:rw" \
					-v $(shell pwd):/data \
					-w=/data \
					--env IS_CI=$(IS_CI) \
					--env WHO=$(WHO) \
					375412324511.dkr.ecr.us-west-2.amazonaws.com/cd/python-build-tool:0.1

PYTHON_39_IT := docker run -it \
					-v "/var/run/docker.sock:/var/run/docker.sock:rw" \
					-v $(shell pwd):/data \
					-w=/data \
					-v ~/.aws:/tmp \
					-v ~/.ssh:/root/.ssh:ro \
					--env AWS_PROFILE=$(AWS_PROFILE) \
					--env AWS_SHARED_CREDENTIALS_FILE=/tmp/credentials \
					--env AWS_CONFIG_FILE=/tmp/config \
					--env IS_CI=$(IS_CI) \
					--env WHO=$(WHO) \
					375412324511.dkr.ecr.us-west-2.amazonaws.com/cd/python-build-tool:0.1
