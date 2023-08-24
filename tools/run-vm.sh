#!/bin/bash

name=$1
disk=$2
if [ -z $name ]; then
  name=apt-ostree
fi

virt-install \
	--connect qemu:///system \
	--boot loader=/usr/share/ovmf/OVMF.fd \
	--machine q35 \
	--name $name \
	--ram 8096 \
	--vcpus 4 \
	--os-variant debiantesting \
	--disk path=$disk/debian-ostree-qemu-uefi-amd64.img \
	--noautoconsole \
	--check path_in_use=off \
	--import
