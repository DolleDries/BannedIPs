#!/usr/bin/env python
##

import os
import re
import sys
import pickle
#import socket
#import tempfile
#import argparse
from ipwhois.experimental import get_bulk_asn_whois
from ipwhois.experimental import bulk_lookup_rdap
from pprint import pprint

#IPsort = lambda a1, a2: cmp(socket.inet_aton(a1), socket.inet_aton(a2))

#IPlist = []


def Remember(It, As):
    """Make findings reuseable"""
    storage = os.path.join(tempfile.gettempdir(), As)
    with open(storage, 'wb') as f:
        pickle.dump(It, f)

def Recall(tale):
    """Recall findings"""
    It = []
    storage = os.path.join(tempfile.gettempdir(), tale)
    with open(storage, 'rb') as f:
        It = pickle.load(f)
    return It

def MyWhoIs(IPlist):
    """Reformat whois_list"""
    results = get_bulk_asn_whois(addresses=IPlist)
    #pprint(results.split('\n'))
    Grumble = results.split('\n')
    return Grumble
    # pprint(Grumble)

if __name__ == "__main__":
    import argparse
    import IPsort

    parser = argparse.ArgumentParser(description="Grok file....")
    parser.add_argument('file', help='File do do magic on')
    parser.add_argument('-s', '--separator', type=str, help='Seperator', default=';')
    args = parser.parse_args()
    file = args.file
    sep = args.separator
    
    list = IPsort.do_magic(file, sep)
    result = MyWhoIs(list)

    pprint(result)
    #Filename = "%s.json" % key
    #with open(Filename, 'w') as outfile:
    #    json.dump(result, outfile, sort_keys=True, indent=4)

    #for item in result:
        #print "%s" % (item)

