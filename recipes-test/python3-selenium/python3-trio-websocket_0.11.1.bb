
SUMMARY = "WebSocket library for Trio"
HOMEPAGE = "https://github.com/python-trio/trio-websocket"
AUTHOR = "Mark E. Haase <mehaase@gmail.com>"
LICENSE = "MIT"
LIC_FILES_CHKSUM = "file://LICENSE;md5=69a70f9681c723a2b4bc1afb1fc68a6f"

SRC_URI[sha256sum] = "18c11793647703c158b1f6e62de638acada927344d534e3c7628eedcb746839f"

RDEPENDS:${PN} = "python3-trio python3-wsproto"

inherit setuptools3 pypi
