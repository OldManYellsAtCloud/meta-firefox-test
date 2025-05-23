#!/bin/bash

if [ $# -le 3 ]; then
  echo Usage: $0 yocto_version arch ff_version [lic_flavour]
  echo E.g. $0 kirkstone aarch64 esr
  exit 1
fi

declare -A arch_qemu_dict
arch_qemu_dict["arm"]="qemuarm"
arch_qemu_dict["aarch64"]="qemuarm64"
arch_qemu_dict["riscv"]="qemuriscv64"
arch_qemu_dict["x86-64"]="qemux86-64"

yocto_version=$1
arch=$2
ff_version=$3
libc_flavour=$4

kas_file_name=$yocto_version-$ff_version-$arch

if [ -n "$libc_flavour" ]; then
  kas_file_name=$libc_flavour-$kas_file_name
else
  kas_file_name=glibc-$kas_file_name
fi

# check if it needs to be built, if the flag has been set
if [ -d /yocto/test-images/$kas_file_name ]; then
  echo Image has been already built, exiting.
  exit 0
fi

cd /yocto/$yocto_version

if [ "$arch" = "riscv" ]; then
  OPENSBI="opensbi"
else
  OPENSBI=""
fi

qemu_machine=${arch_qemu_dict[$arch]}

rm -rf ./build/tmp/deploy/images/$qemu_machine

kas checkout --update ./meta-firefox-test/kas/$kas_file_name-test.yml || exit 1
kas shell ./meta-firefox-test/kas/$kas_file_name-test.yml -c "bitbake -c clean rust-native cargo-native libstd-rs firefox \
         rust-llvm-native \
         firefox-l10n-ach          firefox-l10n-en-gb  firefox-l10n-hi-in  firefox-l10n-ms     firefox-l10n-sr \
         firefox-l10n-af           firefox-l10n-en-us  firefox-l10n-hr     firefox-l10n-my     firefox-l10n-sv-se \
         firefox-l10n-an           firefox-l10n-eo     firefox-l10n-hsb    firefox-l10n-nb-no  firefox-l10n-szl \
         firefox-l10n-ar           firefox-l10n-es-ar  firefox-l10n-hu     firefox-l10n-ne-np  firefox-l10n-ta \
         firefox-l10n-ast          firefox-l10n-es-cl  firefox-l10n-hy-am  firefox-l10n-nl     firefox-l10n-te \
         firefox-l10n-az           firefox-l10n-es-es  firefox-l10n-ia     firefox-l10n-nn-no  firefox-l10n-tg \
         firefox-l10n-be           firefox-l10n-es-mx  firefox-l10n-id     firefox-l10n-oc     firefox-l10n-th \
         firefox-l10n-bg           firefox-l10n-et     firefox-l10n-is     firefox-l10n-pa-in  firefox-l10n-tl \
         firefox-l10n-bn           firefox-l10n-eu     firefox-l10n-it     firefox-l10n-pl     firefox-l10n-tr \
         firefox-l10n-br           firefox-l10n-fa     firefox-l10n-ja     firefox-l10n-pt-br  firefox-l10n-trs \
         firefox-l10n-bs           firefox-l10n-ff     firefox-l10n-ka     firefox-l10n-pt-pt  firefox-l10n-uk \
         firefox-l10n-ca           firefox-l10n-fi     firefox-l10n-kab    firefox-l10n-rm     firefox-l10n-ur \
         firefox-l10n-cak          firefox-l10n-fr     firefox-l10n-kk     firefox-l10n-ro     firefox-l10n-uz \
         firefox-l10n-ca-valencia  firefox-l10n-fur    firefox-l10n-km     firefox-l10n-ru     firefox-l10n-vi \
         firefox-l10n-cs           firefox-l10n-fy-nl  firefox-l10n-kn     firefox-l10n-sc     firefox-l10n-xh \
         firefox-l10n-cy           firefox-l10n-ga-ie  firefox-l10n-ko     firefox-l10n-sco    firefox-l10n-zh-cn \
         firefox-l10n-da           firefox-l10n-gd     firefox-l10n-lij    firefox-l10n-si     firefox-l10n-zh-tw \
         firefox-l10n-de           firefox-l10n-gl     firefox-l10n-lt     firefox-l10n-sk     firefox-l10n-dsb \
         firefox-l10n-gn           firefox-l10n-lv     firefox-l10n-sl     firefox-l10n-el     firefox-l10n-gu-in \
         firefox-l10n-mk           firefox-l10n-son    firefox-l10n-en-ca  firefox-l10n-he     firefox-l10n-mr \
         firefox-l10n-sq virtual/kernel $OPENSBI" || exit 1
kas build ./meta-firefox-test/kas/$kas_file_name-test.yml || exit 1

cp -r ./build/tmp/deploy/images/$qemu_machine /yocto/test-images/$kas_file_name
