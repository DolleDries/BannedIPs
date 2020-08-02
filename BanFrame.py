#!/usr/bin/env python
#

__version__ = '''$Id: Frames.py 129 2010-08-24 11:49:23Z andre $'''

import sys, os, time
import cgi
import re

#import cgitb; cgitb.enable(); print "Content-Type: text/html"; print

import HTMLgen


menu = HTMLgen.Frame(name='panel', src='Menu.py', noresize=1)
content = HTMLgen.Frame(name='body', src='BAN.html', noresize=1)
page = HTMLgen.Frameset(menu, content, cols='250,*', frameborder="0", border="0", framespacing="0")
doc = HTMLgen.FramesetDocument()
doc.title = "Banned Ipno's"
#doc.meta = MetaTags
doc.append(page)

print "Content-Type: text/html"
print
print doc
