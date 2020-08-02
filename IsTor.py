#!/usr/bin/env python
##

import os
import re
import sys
import pickle
import tempfile
import requests
import time
import json

TORLIST_URL = "https://www.dan.me.uk/torlist/"
keep = False

def IsTor(IP):

    """
    Get a TORlist. Save it and if a gine IPno is in that list. Not mine.
    See https://www.dan.me.uk/tornodes for details.
    """
    IP = IP.strip()
    tl_path = os.path.join(tempfile.gettempdir(), 'TORlist.pickle')
    try:
        with open(tl_path, 'r') as infile:
            tl = pickle.load(infile)
            if keep:
                with open('TORlist.pickle', 'w') as outfile:
                    json.dump(tl, outfile, sort_keys=True, indent=4)
    except IOError as e:
        req = requests.get(TORLIST_URL)
        if req:
            tl = req.text.split('\n')
            
            with open(tl_path, 'w') as outfile:
                #json.dump(tl, outfile, sort_keys=True, indent=4)
                pickle.dump(tl, outfile)
        else:
            print req.text.split('\n')
            print time.ctime()
            future = time.time() + 1800
            print time.ctime(future)
            sys.exit()
            #print req.status

    #print tl
    #sys.exit()
    
    if IP not in tl:
        return False
    else:
        return True

if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser(description="Tetsing 'argparse...")
    group = parser.add_mutually_exclusive_group()
    group.add_argument('-i', '--input', help='FILE')
    group.add_argument('-a', '--address', help='IPno')
    parser.add_argument('-k', '--keep', action="store_true", help='Keep TORlist.json (copy it to /tmp if needed).')
    args = parser.parse_args()
    print args

    keep = args.keep
    address = args.address
    file = args.input

    if file:
        input = open(file, "r")
    
    if address:
        print "%s  (%s)" % ( address, "TOR" if IsTor(address) else 'Nope')
    if file != None:
        for address in input.readlines():
            address = re.sub("\n", "", address)              #Reduce surplus of newline and carriage return
            print "%s  (%s)" % ( address, "TOR" if IsTor(address) else 'Nope')
