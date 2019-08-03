#!/bin/bash
if [[ $(which docker) != '' ]]
then
	CMD=docker
else
	CMD=podman
fi
$CMD build -t imiell/vultr-bare-metal .
$CMD push imiell/vultr-bare-metal
