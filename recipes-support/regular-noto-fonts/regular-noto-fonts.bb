DESCRIPTION = "Google noto fonts"
LICENSE = "OFL-1.1"
LIC_FILES_CHKSUM = "file://${COMMON_LICENSE_DIR}/OFL-1.1;md5=fac3a519e5e9eb96316656e0ca4f2b90"

SRC_URI = "https://noto-website-2.storage.googleapis.com/pkgs/Noto-unhinted.zip"

SRC_URI[md5sum] = "d26b29b10c3c8d05df4ade8286963722"
SRC_URI[sha256sum] = "7d0e099c208d11d7bf64091ea7f62f85bc07dedfaf2c01de53985a5b981025e3"

UNPACKDIR = "${S}"

inherit allarch fontcache

FILES:${PN} += " \
    ${datadir}/fonts/noto/* \
"

do_install() {
        cd ${S}
        for f in `ls *Regular*`; do
                install -Dm 0644 $f ${D}${datadir}/fonts/noto/$f
        done
}

do_compile[noexec] = "1"

ALLOW_EMPTY:${PN} = "1"
INHIBIT_DEFAULT_DEPS = "1"
