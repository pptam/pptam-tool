# Installation using virtual machines

To install PPTAM on *Windows* we first performed the following installation steps:

- we activated the Linux Subsystem, installing the *Ubuntu* distribution (e.g., following [this](https://www.windowscentral.com/install-windows-subsystem-linux-windows-10) instructions);
- 

vboxmanage list vms
VBoxManage modifyvm "Ubuntu 20.04 Server" --nested-hw-virt on
config.vm.boot_timeout

