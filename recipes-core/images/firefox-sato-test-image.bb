require recipes-sato/images/core-image-sato.bb
require firefox-test-image.inc

fix_resolution(){
  sed -i 's/Modes.*/Modes \"1024x600\"/g' ${IMAGE_ROOTFS}${sysconfdir}/X11/xorg.conf || true
}

ROOTFS_POSTPROCESS_COMMAND += ";fix_resolution;"
