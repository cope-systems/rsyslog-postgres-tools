# https://stackoverflow.com/a/18137056
base_dir := $(shell dirname "$(abspath $(lastword $(MAKEFILE_LIST)))")

test:
	"${base_dir}/scripts/test.sh" $(ARGS)

build:
	"${base_dir}/scripts/build.sh" $(ARGS)

run_containerized:
	"${base_dir}/scripts/run_containerized.sh" $(ARGS)
