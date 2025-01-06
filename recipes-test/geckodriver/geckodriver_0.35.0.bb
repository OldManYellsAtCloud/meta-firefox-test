LICENSE = "MPL-2.0"
LIC_FILES_CHKSUM = "file://LICENSE;md5=f928f8708435b11c19e5690af9ad7f95"

# This SRC_URI requires "bad-src-uri" to be added to INSANE_SKIP:pn-geckodriver,
# but on global config level (local.conf, etc), otherwise it fails
# before it would parse INSANE_SKIP in this recipe.
# The original source is stored in a Mercurial SCM, but Mercurial
# support is broken on multiple places in Yocto, when using
# modern Python, so instead of taking a deepdive into that, I took the
# bad, however easy solution.

SRC_URI = "https://github.com/mozilla/geckodriver/archive/refs/tags/v${PV}.tar.gz"
SRC_URI[sha256sum] = "5e77314806e275daeed70acb04b56c039060a13a2394df832127708e89708163"

include geckodriver-crates.inc

inherit cargo 
# cargo-update-recipe-crates class doesn't exist in Kirkstone
# so let me just keep this here, and set it manually, when
# it comes to updating it.
# cargo-update-recipe-crates

UNPACKDIR = "${S}"
# CARGO_SRC_DIR = "${PN}-${PV}"
