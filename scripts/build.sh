#!/bin/bash

if [ $# -ne 5 ]; then
  echo Usage: $0 yocto_version arch ff_version libc_flavour toolchain display_system
  echo E.g. $0 wrynose aarch64 esr glibc wayland
  echo Available values:
  echo libc_flavour: glibc, musl
  echo display_system: wayland, x11
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
display_system=$5

echo Yocto version: ${yocto_version}
echo Arch: ${arch}
echo Firefox version: ${ff_version}
echo Libc Flavour: ${libc_flavour}
echo Display system: ${display_system}

main_kas_file_name=$yocto_version-$arch
main_kas_file_path=./meta-firefox-test/kas/${main_kas_file_name}-test.yml
result_name=$yocto_version-$ff_version-$arch
libc_file_path=./meta-firefox-test/kas/${libc_flavour}.yml
ff_file_path=./meta-firefox-test/kas/ff/${ff_version}.yml
display_file_path=./meta-firefox-test/kas/${display_system}.yml

# check if it needs to be built, if the flag has been set
if [ -d /yocto/test-images/$result_name ]; then
  echo Image has been already built, exiting.
  exit 0
fi

cd /yocto/$yocto_version

if [ "$arch" = "riscv" ]; then
  OPENSBI="opensbi"
else
  OPENSBI=""
fi

if [ "$yocto_version" = "master" -o "$yocto_version" = "wrynose" ]; then
  RUST_LLVM=""
  if [ "$arch" = "arm" -a "$libc_flavour" = "musl" -a "$display_system" = "x11" ]; then
    MUSL_ARM_CORRECTION=":./meta-firefox-test/kas/musl-arm32-distro-features.yml"
  else
    MUSL_ARM_CORRECTION=""
  fi
else
  RUST_LLVM="rust-llvm-native"
fi

qemu_machine=${arch_qemu_dict[$arch]}

rm -rf ./build/tmp/deploy/images/$qemu_machine

echo Kas config composition: ${main_kas_file_path}:${libc_file_path}:${display_file_path}:${ff_file_path}${MUSL_ARM_CORRECTION}

kas checkout --update ${main_kas_file_path}:${libc_file_path}:${display_file_path}:${ff_file_path}${MUSL_ARM_CORRECTION} || exit 1
kas shell ${main_kas_file_path}:${libc_file_path}:${display_file_path}:${ff_file_path}${MUSL_ARM_CORRECTION} -c "bitbake -c clean rust-native cargo-native libstd-rs firefox \
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
         firefox-l10n-sq virtual/kernel $OPENSBI $RUST_LLVM" || exit 1
kas shell ${main_kas_file_path}:${libc_file_path}:${display_file_path}:${ff_file_path}${MUSL_ARM_CORRECTION} -c "bitbake llvm-native"
kas shell ${main_kas_file_path}:${libc_file_path}:${display_file_path}:${ff_file_path}${MUSL_ARM_CORRECTION} -c "bitbake llvm"
kas shell ${main_kas_file_path}:${libc_file_path}:${display_file_path}:${ff_file_path}${MUSL_ARM_CORRECTION} -c "bitbake nodejs-native"
kas build ${main_kas_file_path}:${libc_file_path}:${display_file_path}:${ff_file_path}${MUSL_ARM_CORRECTION} || exit 1

cp -r ./build/tmp/deploy/images/$qemu_machine /yocto/test-images/$result_name

echo Libc flavour: ${libc_flavour} >> /yocto/test-images/${result_name}.info
echo Display system: ${display_system} >> /yocto/test-images/${result_name}.info
