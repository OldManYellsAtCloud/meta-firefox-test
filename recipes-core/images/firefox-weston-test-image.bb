require recipes-graphics/images/core-image-weston.bb
require firefox-test-image.inc

disable_screenlock(){
  sed -i '8i idle-time=0' ${IMAGE_ROOTFS}${sysconfdir}/xdg/weston/weston.ini
  echo [shell] >> ${IMAGE_ROOTFS}${sysconfdir}/xdg/weston/weston.ini
  echo locking=false >> ${IMAGE_ROOTFS}${sysconfdir}/xdg/weston/weston.ini
}

ROOTFS_POSTPROCESS_COMMAND += ";disable_screenlock;"
