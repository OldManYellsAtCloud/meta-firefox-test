
SUMMARY = "Capture the outcome of Python function calls."
HOMEPAGE = "https://github.com/python-trio/outcome"
AUTHOR = "Frazer McLean <frazer@frazermclean.co.uk>"
LICENSE = "MIT"
LIC_FILES_CHKSUM = "file://LICENSE;md5=fa7b86389e58dd4087a8d2b833e5fe96"

SRC_URI[sha256sum] = "9dcf02e65f2971b80047b377468e72a268e15c0af3cf1238e6ff14f7f91143b8"

RDEPENDS:${PN} = "python3-attrs"

inherit setuptools3 pypi
