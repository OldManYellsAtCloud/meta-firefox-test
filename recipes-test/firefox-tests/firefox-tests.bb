DESCRIPTION = "Sanity checks for Firefox browser"
LICENSE = "MIT"
LIC_FILES_CHKSUM = "file://${COMMON_LICENSE_DIR}/MIT;md5=0835ade698e0bcf8506ecda2f7b4f302"

RDEPENDS = "firefox python3-pytest"

SRC_URI = "file://run.sh \
           file://smoke \
           file://language"

UNPACKDIR = "${S}"

do_install(){
  install -Dm 0755 ${S}/run.sh ${D}/home/root/run.sh
  cp -r ${S}/smoke ${D}/home/root/
  cp -r ${S}/language ${D}/home/root/
}

FILES:${PN} = "/home/root/run.sh \
               /home/root/smoke/* \
               /home/root/language/*"
