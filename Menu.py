#!/usr/bin/env python

import os
import sys
import datetime

import HTMLgen
from HTMLcolors import *

##
# HvD -- Ha! :)
Created = datetime.datetime.fromtimestamp(os.path.getmtime('Oops.json')).strftime("%d %B %Y")
Kopje = HTMLgen.Heading(4, Created)

#doc = HTMLgen.SimpleDocument( 'HTML.rc' ) 
doc = HTMLgen.SeriesDocument('Menu.rc')
#doc.place_nav_buttons = 'no'

S = HTMLgen.Strong()
C = HTMLgen.Center()
BR = HTMLgen.BR()


AboutTxt = HTMLgen.RawText("""
    During the COVID pandemic there was an explosion in SSH
    connection attempts. A big list didn't give much insight. So I
    created a few (python) scripts for generating a JSON file which I could
    feed to a
    <a href=https://github.com/vasturiano/circlepack-chart>circlepacking</a>
    module.<br>
    This is the result.<br>
    Circles are  zoomable, at the non-world levels dragable.<br>
    A mouseover reveals textual info.<br>
    <a
    href=http://www.tabellenboekje.nl/landcodes-tabel-2-letter.php#sortering-code>Country codes</a>
""")

MiscTxt = HTMLgen.RawText("""
    Got errors on Korea.<br>
    Made a minor change in .../ipwhois/nir.py line 111.<br>
    changed to: 'url': 'https://xn--c79as89aj0e29b77z.xn--3e0b707e/eng/main.jsp',
""")

TodoTxt = HTMLgen.RawText("""
    Lots...<br>
    Give a 'TOR-color' to tor-exitnodes.<br>
    Make labels more visible.<br>
    Use GeoIP(?)<br>
    Use canvas(?)<br>
    Make a history view(?)<br>
    Create a search thing(?)<br>
""")

ContactTxt =  HTMLgen.RawText( """
    andrevandervlies[at]gmail[dot]com
    vastur[at]gmail[dot]com <a href=https://github.com/vasturiano/circlepack-chart target=BODY>github</a>
""")

SourcesTxt = HTMLgen.RawText("""
    http://vandervlies.xs4all.nl/~andre/BAN/src
""")

Table = HTMLgen.TableLite( CLASS='menu' )

ChoiceList = [('About', 'caption', ''),
              ('About', 'info', AboutTxt),
              ('Misc', 'caption', ''),
              ('Misc', 'info', MiscTxt),
              ('Todo', 'caption', ''),
              ('Todo', 'info', TodoTxt),
              ('Contact', 'caption', ''),
              ('Contact', 'info', ContactTxt),
              ('Sources', 'caption', ''),
              ('Sources', 'url', SourcesTxt),
            ]

for (item, kind, content) in ChoiceList:
    if kind == 'caption':
        cell = [ HTMLgen.TD(item, CLASS='menuhead') ]
    elif kind == 'url':
        contents = HTMLgen.Href(url=content, text=item, target='body')
        #contents.append(info)
        cell = [ HTMLgen.TD(contents, CLASS='menuoption') ]
    elif kind == 'info':
        cell = [ HTMLgen.TD(content, CLASS='menuinfo') ]
        
    row = HTMLgen.TR()
    row = row + cell
    Table.append(row)

#pragma = HTMLgen.Meta(equiv='PRAGMA', content='NO-CACHE')
#doc.append(pragma)

doc.append(Kopje)
doc.append( HTMLgen.BR() )
doc.append( Table )

print """Content-type: text/html"""
print
print doc
