#!/bin/bash

if [ $? -ne 2 ]; then
  echo Usage: $0 yocto_version arch ff_version
  echo E.g. $0 scarthgap x86_64 esr
fi

declare -A arch_qemu_dict
arch_qemu_dict["arm"]="qemuarm"
arch_qemu_dict["aarch64"]="qemuarm64"
arch_qemu_dict["riscv"]="qemuriscv64"
arch_qemu_dict["x86_64"]="qemux86_64"

yocto_version=$1
arch=$2
ff_version=$3

cd /yocto/$yocto_version
source poky/oe-init-build-env

coproc qemu { runqemu $qemu_machine; }

TIMEOUT=60
QEMU_ONLINE="false"
while [ $TIMEOUT -gt 0 -a "$QEMU_ONLINE" = "false" ]; do
  # keep probing the machine, until it's ready for ssh connection
  ssh root@192.168.7.4 -o 'BatchMode=yes' -o 'ConnectionAttempts=1' true
  if [ $? -eq 0 ]; then
    QEMU_ONLINE="true"
  else
    sleep 3
    TIMEOUT=$((TIMEOUT-5))
  fi
done

if [ "$QEMU_ONLINE" = "false" ]; then
  echo QEMU is still offline!
  exit 1
fi

# run test
ssh root@192.168.7.4 -o 'BatchMode=yes' /home/root/run.sh smoke

# run languagetest, if it hasn't been executed yet
if [ ! -e /yocto/test-images/language-test ]; then
  ssh root@192.168.7.4 -o 'BatchMode=yes' /home/root/run.sh language
  touch /yocto/test-images/language-test
fi

# move the test results over here
mkdir -p /yocto/test-images/$yocto_version-$arch-$ff_version
scp root@192.168.7.4:~/*xml /yocto/test-images/$yocto_version-$arch-$ff_version/

kill $qemu_PID
