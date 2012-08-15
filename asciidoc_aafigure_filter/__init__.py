#! /usr/bin/env python
"""AsciiDoc filter script which runs the aafigure program to
convert ASCII line drawings into either a SVG or PNG image file.

Requires the aafigure Python package and Python Imaging Library (PIL) packages
to be installed.

Copyright (C) 2011 Henrik Maier. Free use of this software is
granted under the terms of the GNU General Public License (GPL).

Modified by Jeremy Hughes <jedahu@gmail.com> to be an in-process filter.
"""

__version__ = '1.2'

# Suppress warning: "the md5 module is deprecated; use hashlib instead"
import warnings
warnings.simplefilter('ignore',DeprecationWarning)

import os, sys, md5
from optparse import *

# Import aafigure which must be installed as Python package.
# Tested with aafigure 0.5
import aafigure, aafigure.svg, aafigure.pil

from StringIO import StringIO
from base64 import b64encode


#
# Helper functions and classes
#
class AppError(Exception):
    """Application specific exception."""
    pass



#
# Customised aafigure classes
#
class WidthHeightSVGOutputVisitor(aafigure.svg.SVGOutputVisitor):
    '''Modfied version of SVG output visitor class which inserts width/height'''
    def visit_image(self, aa_image):
        return aafigure.svg.SVGOutputVisitor.visit_image(self, aa_image, xml_header=False)


#
# Application init and logic
#
class Application():
    """Application class"""

    def __init__(self,
            lines,
            verbose=False,
            format='svg',
            scaling='1.0',
            aspect='1.0',
            linewidth='2.0',
            foreground='#000000',
            background='#ffffff',
            fill='#000000',
            opts=(),
            backend=None,
            **kwargs):
        """Process commandline arguments"""
        print 'OPTS:', opts
        self.backend = backend
        self.lines = lines
        self.verbose = verbose
        self.outfile = StringIO()
        self.format = format
        self.scaling = float(scaling)
        self.aspect = float(aspect)
        self.linewidth = float(linewidth)
        self.foreground = foreground
        self.background = background
        self.fill = fill
        self.textual = 'textual' in opts
        self.proportional = 'fixed' not in opts

        self.print_verbose("Output format is %s" % str.upper(self.format))

    def run(self):
        """Core logic of the application"""
        if self.format == 'svg':
            font = None # Embed no font info for SVGs, SVGs use font-family attribute
            visitor = WidthHeightSVGOutputVisitor
        else:
            # Be specific about fonts with PNGs as font files are otherwise platform specific
            if self.proportional:
                font = os.path.join(os.path.dirname(os.path.realpath(sys.argv[0])),
                                    "LiberationSans-Regular.ttf")
            else:
                font = os.path.join(os.path.dirname(os.path.realpath(sys.argv[0])),
                                    "LiberationMono-Regular.ttf")
            visitor = aafigure.pil.PILOutputVisitor
        aafigure.process(unicode('\n'.join(self.lines), 'utf-8'), visitor,
                         options={'file_like': self.outfile,
                                  'proportional': self.proportional,
                                  'textual': self.textual,
                                  'line_width': self.linewidth,
                                  'scale': self.scaling,
                                  'aspect': self.aspect,
                                  'fill': self.fill,
                                  'foreground': self.foreground,
                                  'background': self.background,
                                  'format':self.format,
                                  'font': font
                                  })

    def print_verbose(self, line):
        if self.verbose:
            sys.stderr.write(line + os.linesep)


def asciidoc_filter(lines, **kwargs):
    if kwargs.get('backend').find('html') < 0:
        raise Exception, 'Not implemented for non html backends.'
    app = Application(lines, **kwargs)
    app.run()
    app.outfile.seek(0)
    out = None
    if kwargs.get('format') == 'png':
        out = 'data:image/png;base64,' + b64encode(app.outfile.getvalue())
    else:
        out = 'data:image/svg+xml;base64,' + b64encode(app.outfile.getvalue())
    return [out]
