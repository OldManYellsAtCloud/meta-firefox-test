
SUMMARY = "WebSockets state-machine based protocol implementation"
HOMEPAGE = "https://github.com/python-hyper/wsproto/"
AUTHOR = "Benno Rice <benno@jeamland.net>"
LICENSE = "MIT"
LIC_FILES_CHKSUM = "file://LICENSE;md5=69fabf732409f4ac61875827b258caaf"

SRC_URI[sha256sum] = "ad565f26ecb92588a3e43bc3d96164de84cd9902482b130d0ddbaa9664a85065"

RDEPENDS:${PN} = "python3-h11"

inherit setuptools3 pypi
