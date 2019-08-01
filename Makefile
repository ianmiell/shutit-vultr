help:
	@echo 'make run    - run the knative bmachine up'
	@echo 'make build  - build the image'

.PHONY: help run access build container_run backup restore check_host check_container check_nodiff

run:
	python run.py

build:
	./build.sh
