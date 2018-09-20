#!/usr/bin/env python
# coding=utf-8
import os

GRUB_FILE = '/etc/default/grub'

def get_grub_file():
	with open(GRUB_FILE, 'r') as f:
		grub_content = f.read()
	f.closed
	return grub_content

def set_grub_file(new_grub_content):
	grub_file = open(GRUB_FILE, 'w')
	grub_file.write(new_grub_content)
	grub_file.close()

def check_grub_conf(grub_content):
	if grub_content.find("net.ifnames=0 biosdevname=0") > 0:
		return True
	return False

def set_eth0_conf(grub_content):
	return grub_content.replace("GRUB_CMDLINE_LINUX=\"\"", "GRUB_CMDLINE_LINUX=\"net.ifnames=0 biosdevname=0\"")

if __name__ == '__main__':

	grub_content = get_grub_file()

	if check_grub_conf(grub_content) is False:
		new_grub = set_eth0_conf(grub_content)
		set_grub_file(new_grub)
		os.system("sudo update-grub")
		os.system("sleep 1")
		os.system("sudo reboot")