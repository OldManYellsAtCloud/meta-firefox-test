DESCRIPTION = "Sanity checks for Firefox browser"
LICENSE = "MIT"
LIC_FILES_CHKSUM = "file://${COMMON_LICENSE_DIR}/MIT;md5=0835ade698e0bcf8506ecda2f7b4f302"

RDEPENDS:${PN} = "firefox python3-pytest geckodriver python3-selenium"

SRC_URI = "file://run.sh \
           file://smoke \
           file://language"

do_install(){
  if [ -e ${UNPACKDIR}/run.sh ]; then
    install -Dm 0755 ${UNPACKDIR}/run.sh ${D}/home/root/run.sh
    cp -r ${UNPACKDIR}/smoke ${D}/home/root/
    cp -r ${UNPACKDIR}/language ${D}/home/root/
  else
    install -Dm 0755 ${WORKDIR}/run.sh ${D}/home/root/run.sh
    cp -r ${WORKDIR}/smoke ${D}/home/root/
    cp -r ${WORKDIR}/language ${D}/home/root/
  fi
}

FILES:${PN} = "/home/root/run.sh \
               /home/root/smoke/* \
               /home/root/language/*"
