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

cd /yocto/$yocto_version/poky
source oe-init-build-env ../build

rm -rf tmp/deploy/images/$qemu_machine
cp -r /yocto/test-images/$image_folder tmp/deploy/images/$qemu_machine

sed -i "s/8.8.8.8/192.168.1.59/g" tmp/deploy/images/$qemu_machine/firefox-test-image*conf

coproc qemu { runqemu "$qemu_machine $qemu_params"; }

TIMEOUT=100
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

touch /yocto/test-images/$image_folder.done

# move the test results over here
mkdir -p /yocto/test-images/$image_folder/test-results
mkdir -p /yocto/$yocto_version/meta-browser/meta-firefox/test-results

scp root@$guest_side_ip:~/*xml /yocto/test-images/$image_folder/test-results
ssh root@$guest_side_ip -o 'BatchMode=yes' shutdown -h now

# check if anything has failed
ERRORS=`grep -v 'failures="0"' /yocto/test-images/$image_folder/test-results/*xml`

if [ -z "$ERRORS" ]; then
  RET=0
else
  RET=1
fi

kill $qemu_PID

exit $RET
