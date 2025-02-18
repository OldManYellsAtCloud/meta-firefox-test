
SUMMARY = "Official Python bindings for Selenium WebDriver"
HOMEPAGE = "https://www.selenium.dev"
AUTHOR = "None <None>"
LICENSE = "Apache-2.0"
LIC_FILES_CHKSUM = "file://LICENSE;md5=fc85982553603542b7c1fc0ffa7e4fc7"


SRC_URI = "https://files.pythonhosted.org/packages/44/8c/62c47c91072aa03af1c3b7d7f1c59b987db41c9fec0f158fb03a0da51aa6/selenium-4.27.1.tar.gz \
           file://0001-selenium-rust-don-t-abort-on-panic.patch"

SRC_URI[md5sum] = "ccb1b28eb5e4fca361263742ab9f6b08"

include python3-selenium-crates.inc

S = "${WORKDIR}/selenium-4.27.1"

RDEPENDS:${PN} = "python3-urllib3 python3-trio python3-trio-websocket python3-certifi python3-typing-extensions python3-websocket-client"

inherit python_setuptools3_rust 
# cargo-update-recipe-crates

INSANE_SKIP:${PN} = "already-stripped"

do_install:append(){
  if [ -d ${D}${PYTHON_SITEPACKAGES_DIR}/UNKNOWN-0.0.0.dist-info ]; then
    mv ${D}${PYTHON_SITEPACKAGES_DIR}/UNKNOWN-0.0.0.dist-info ${D}${PYTHON_SITEPACKAGES_DIR}/selenium-${PV}.dist-info
  fi
  cd ${S}/selenium
  find . -type f -exec install -D -m 0644 {} ${D}${PYTHON_SITEPACKAGES_DIR}/selenium/{} \;
}
