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
arch_qemu_dict["x86-64"]="qemux86-64"

declare -A qemu_params_dict
qemu_params_dict["x86-64"]='qemuparams=" --enable-kvm "'

yocto_version=$1
arch=$2
ff_version=$3
libc_flavour=$4

if [ -z "$libc_flavour" ]; then
  image_folder=glibc-$yocto_version-$ff_version-$arch
else
  image_folder=$libc_flavour-$yocto_version-$ff_version-$arch
fi

qemu_machine=${arch_qemu_dict[$arch]}
qemu_params="${qemu_params_dict[$arch]}"

if [ ! -d /yocto/test-images/$image_folder ]; then
  echo $image_folder image was not created!
  exit 1
fi

if [ -f /yocto/test-images/$image_folder.done ]; then
  echo $image_folder test done already, skipping now.
  exit 0
fi

cd /yocto/$yocto_version/poky || cd /yocto/$yocto_version/oe-core
source oe-init-build-env ../build

rm -rf tmp/deploy/images/$qemu_machine
cp -r /yocto/test-images/$image_folder tmp/deploy/images/$qemu_machine

sed -i "s/8.8.8.8/192.168.1.59/g" tmp/deploy/images/$qemu_machine/firefox-test-image*conf

coproc qemu { runqemu snapshot "$qemu_machine $qemu_params" > qemu_output 2>&1; }

TIMEOUT=100
QEMU_ONLINE="false"
while [ $TIMEOUT -gt 0 -a "$QEMU_ONLINE" = "false" ]; do
  guest_side_ip=$(grep "Network configuration" ./qemu_output | cut -d= -f2 | cut -d: -f1)

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
mkdir -p /yocto/test-images/$image_folder/test-results
mkdir -p /yocto/$yocto_version/meta-browser/meta-firefox/test-results

scp root@$guest_side_ip:~/*xml /yocto/test-images/$image_folder/test-results
ssh root@$guest_side_ip -o 'BatchMode=yes' /sbin/shutdown -h now

# check if anything has failed
ERRORS=`grep -v 'failures="0"' /yocto/test-images/$image_folder/test-results/*xml`

if [ -z "$ERRORS" ]; then
  touch /yocto/test-images/$image_folder.done
  RET=0
else
  RET=1
fi

kill $qemu_PID

exit $RET
