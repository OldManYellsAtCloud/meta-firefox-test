
SUMMARY = "WebSocket library for Trio"
HOMEPAGE = "https://github.com/python-trio/trio-websocket"
AUTHOR = "Mark E. Haase <mehaase@gmail.com>"
LICENSE = "MIT"
LIC_FILES_CHKSUM = "file://LICENSE;md5=69a70f9681c723a2b4bc1afb1fc68a6f"

SRC_URI = "https://files.pythonhosted.org/packages/dd/36/abad2385853077424a11b818d9fd8350d249d9e31d583cb9c11cd4c85eda/trio-websocket-0.11.1.tar.gz"
SRC_URI[md5sum] = "3d9bb51b62f562dbdbc2ec067132c4a6"
SRC_URI[sha256sum] = "18c11793647703c158b1f6e62de638acada927344d534e3c7628eedcb746839f"

S = "${WORKDIR}/trio-websocket-0.11.1"

RDEPENDS:${PN} = "python3-trio python3-wsproto"

inherit setuptools3
