
SUMMARY = "WebSockets state-machine based protocol implementation"
HOMEPAGE = "https://github.com/python-hyper/wsproto/"
AUTHOR = "Benno Rice <benno@jeamland.net>"
LICENSE = "MIT"
LIC_FILES_CHKSUM = "file://LICENSE;md5=69fabf732409f4ac61875827b258caaf"

SRC_URI = "https://files.pythonhosted.org/packages/c9/4a/44d3c295350d776427904d73c189e10aeae66d7f555bb2feee16d1e4ba5a/wsproto-1.2.0.tar.gz"
SRC_URI[md5sum] = "f64973434117e23d2079460ed64b05c3"
SRC_URI[sha256sum] = "ad565f26ecb92588a3e43bc3d96164de84cd9902482b130d0ddbaa9664a85065"

S = "${WORKDIR}/wsproto-1.2.0"

RDEPENDS:${PN} = "python3-h11"

inherit setuptools3
