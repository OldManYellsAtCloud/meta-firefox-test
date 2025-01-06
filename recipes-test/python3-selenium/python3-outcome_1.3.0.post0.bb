
SUMMARY = "Capture the outcome of Python function calls."
HOMEPAGE = "https://github.com/python-trio/outcome"
AUTHOR = "Frazer McLean <frazer@frazermclean.co.uk>"
LICENSE = "MIT"
LIC_FILES_CHKSUM = "file://LICENSE;md5=fa7b86389e58dd4087a8d2b833e5fe96"

SRC_URI = "https://files.pythonhosted.org/packages/98/df/77698abfac98571e65ffeb0c1fba8ffd692ab8458d617a0eed7d9a8d38f2/outcome-1.3.0.post0.tar.gz"
SRC_URI[md5sum] = "3a626832ac864c95f6054958d0da3011"
SRC_URI[sha256sum] = "9dcf02e65f2971b80047b377468e72a268e15c0af3cf1238e6ff14f7f91143b8"

S = "${WORKDIR}/outcome-1.3.0.post0"

RDEPENDS:${PN} = "python3-attrs"

inherit setuptools3
