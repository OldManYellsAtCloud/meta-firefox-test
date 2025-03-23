#!/bin/bash

if [ $# -le 3 ]; then
  echo Usage: $0 yocto_version arch ff_version [libc_flavour]
  echo E.g. $0 scarthgap x86_64 esr
  exit 1
fi

declare -A arch_qemu_dict
arch_qemu_dict["arm"]="qemuarm"
arch_qemu_dict["aarch64"]="qemuarm64"
arch_qemu_dict["riscv"]="qemuriscv64"
arch_qemu_dict["x86_64"]="qemux86-64"

yocto_version=$1
arch=$2
ff_version=$3
libc_flavour=$4

if [ -n "$libc_flavour" ]; then
  image_folder=glibc-$yocto_version-$ff_version-$arch
else
  image_folder=$libc_flavour-$yocto_version-$ff_version-$arch
fi

qemu_machine=${arch_qemu_dict[$arch]}

if [ ! -d /yocto/test-images/$image_folder ]; then
  echo $image_folder image was not created!
  exit 1
fi

cd /yocto/$yocto_version/poky
source oe-init-build-env ../build

rm -rf tmp/deploy/images/$qemu_machine
cp -r /yocto/test-images/$image_folder tmp/deploy/images/$qemu_machine

coproc qemu { runqemu $qemu_machine; }

TIMEOUT=60
QEMU_ONLINE="false"
while [ $TIMEOUT -gt 0 -a "$QEMU_ONLINE" = "false" ]; do
  tap_iface_name=`ip link show | grep tap | tail -n 1 | cut -d: -f2`
  host_side_ip=`ip -o a show | grep $tap_iface_name | grep -v inet6 | grep -o "192.168.7.[0-9]*" | head -n1`
  last_octet=`echo $host_side_ip | cut -d. -f4`
  guest_side_ip=`echo $host_side_ip | cut -d. -f1-3`
  guest_side_ip="$guest_side_ip".$((last_octet + 1))


  # keep probing the machine, until it's ready for ssh connection
  ssh root@$guest_side_ip -o 'BatchMode=yes' -o 'ConnectionAttempts=1' true
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
ssh root@$guest_side_ip -o 'BatchMode=yes' /home/root/run.sh smoke

# run languagetest, if it hasn't been executed yet
if [ ! -e /yocto/test-images/language-test ]; then
  ssh root@$guest_side_ip -o 'BatchMode=yes' /home/root/run.sh language
  touch /yocto/test-images/language-test
fi

# move the test results over here
mkdir -p /yocto/$yocto_version/meta-browser/meta-firefox/test-results

scp root@$guest_side_ip:~/*xml /yocto/$yocto_version/meta-browser/meta-firefox/test-results
ssh root@$guest_side_ip -o 'BatchMode=yes' shutdown -h now

kill $qemu_PID
