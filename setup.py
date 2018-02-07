#!/usr/bin/env python
#
# $Id: /work/modules/aggdraw/setup.py 1180 2006-02-12T14:24:26.234348Z Fredrik  $
# Setup script for aggdraw
#
# Usage:
#
#   To build in current directory:
#   $ python setup.py build_ext -i
#
#   To build and install:
#   $ python setup.py install
#

import os
import sys

from setuptools import setup, Extension

VERSION = "1.2a3.pmx10"

SUMMARY="High quality drawing interface for PIL."

DESCRIPTION = """
The aggdraw module implements the basic WCK 2D Drawing Interface on
top of the AGG library. This library provides high-quality drawing,
with anti-aliasing and alpha compositing, while being fully compatible
with the WCK renderer.
"""

def add_freetype_config(*freetype_roots):
    aggdraw_ext.define_macros.append(("HAVE_FREETYPE2", None))
    aggdraw_ext.sources.extend([
        "agg2/font_freetype/agg_font_freetype.cpp",
        ])
    id = aggdraw_ext.include_dirs
    ld = aggdraw_ext.library_dirs
    id.append("agg2/font_freetype")
    for freetype_root in freetype_roots:
        id.append(os.path.join(freetype_root, "include"))
        id.append(os.path.join(freetype_root, "include/freetype2"))
        ld.append(os.path.join(freetype_root, "lib"))
    aggdraw_ext.libraries.append("freetype")
    if sys.platform == "win32":
        aggdraw_ext.library_dirs.extend(["kernel32", "user32", "gdi32"])

try:
    # add necessary to distutils (for backwards compatibility)
    from distutils.dist import DistributionMetadata
    DistributionMetadata.classifiers = None
    DistributionMetadata.download_url = None
    DistributionMetadata.platforms = None
except:
    pass

agg_sources = [
    # source code currently used by aggdraw
    # FIXME: link against AGG library instead?
    "agg2/src/agg_arc.cpp",
    "agg2/src/agg_bezier_arc.cpp",
    "agg2/src/agg_curves.cpp",
    "agg2/src/agg_path_storage.cpp",
    "agg2/src/agg_rasterizer_scanline_aa.cpp",
    "agg2/src/agg_trans_affine.cpp",
    "agg2/src/agg_vcgen_contour.cpp",
    # "agg2/src/agg_vcgen_dash.cpp",
    "agg2/src/agg_vcgen_stroke.cpp",
    ]

aggdraw_ext = Extension(
    "aggdraw",
    ["aggdraw.cxx"] + agg_sources,
    include_dirs=['agg2/include'],
)

setup_params = dict(
    name="aggdraw",
    version=VERSION,
    author="Fredrik Lundh",
    author_email="fredrik@pythonware.com",
    classifiers=[
        "Development Status :: 4 - Beta",
        # "Development Status :: 5 - Production/Stable",
        "Topic :: Multimedia :: Graphics",
        ],
    description=SUMMARY,
    download_url="http://www.effbot.org/downloads#aggdraw",
    license="Python (MIT style)",
    long_description=DESCRIPTION.strip(),
    platforms="Python 2.1 and later.",
    url="http://www.effbot.org/zone/aggdraw.htm",
    ext_modules = [
        aggdraw_ext,
    ],
    setup_requires=[
        'hgtools>=2.0,<3.0dev',
    ],
)

if __name__ == '__main__':
    # freetype libs (and headers) must be installed to one of these places
    add_freetype_config('/usr/local', '/usr', '/usr/X11', '../freetype-2.3.4')
    setup(**setup_params)
