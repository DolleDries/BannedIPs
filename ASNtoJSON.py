#!/usr/bin/env python
##

import os
import json
import IsTor
from pprint import pprint

def add( dict, Key, Value ):
    """Add a Key (empty list) to a dict. Or a Value to an exsiting Key."""
    if Key not in dict:
        dict[Key] = []
        dict[Key].append(Value)
    else:
        dict[Key].append(Value)

def add_ng( dict, Country, Cidr, Value ):
    """Add a Cidr (empty list) to a County (dict). Or a Value to an exsiting Country.Cidr Key."""
    if Country not in dict:
        dict[Country] = {}
    if Cidr not in dict[Country]:
        dict[Country][Cidr] = []
    dict[Country][Cidr].append(Value)

def Add_Country(Dict, Nation):
    """Add a Country (empty list) to a Childrenlist (of dicts)..."""
    #print "Add_Country: %s" % (Nation)
    Dict['children'].append( { 'name': Nation, 'children': [] } )

def Add_Cidr(Dict, Block, NatIdx):
    """Add a Cidrblock (empty list) to a Childrenlist (of dicts)..."""
    #print "Add_Cidr: %s (%d)" % (Block, NatIdx)
    Dict['children'][NatIdx]['children'].append( { 'name': Block, 'children': [] } )

def Add_Host(Dict, IpNo, NatIdx, CidrIdx):
    """Add a Host to a Childrenlist..."""
    #print "Add_Host: %s (%d %d)" % (IpNo, NatIdx, CidrIdx)
    try:
        Dict['children'][NatIdx]['children'][CidrIdx]['children'].append(IpNo)
    except IndexError as e:
        print "ERROR!!  NatIdx: %d, CidrIdx %s\n%s" % (NatIdx, CidrIdx, e)

def Rebuild(This):
    """Rebuild This (dict) to a JSON circlechart understands..."""
    W = {}
    W['name'] = 'World'
    W['children'] = []

    print "Rebuilding..."
    #pprint(This)
    nation_index = cidr_index = -1           # (list)Indexes start on zero... Preseeding with -1 helps....

    for country, V in This.items():
        nation_index +=1 
        cidr_index = -1                      # New nation, reset cidr block index....
        #print "\t%s" % (country)
        Add_Country(W, country)
        for cidr, I in V.items():
            cidr_index +=1 
            #print "\t\t%s" % (cidr)
            Add_Cidr(W, cidr, nation_index)
            for item in I:                  # This is a list, it needs stepping trough...
                #print "\t\t\t%s" % (item)
                Add_Host(W, item, nation_index, cidr_index)

    return W

def jason(ASNlist):
    """Create a dict and Rebuild it to JSON"""
    result = {}
    print "Doing JaSON..."
    for RawLine in ASNlist:
        try:
            asn, ip, cidr, country, nir, date, desc = RawLine.split('|')
        except:
            continue

        if CheckTOR:
            tor = IsTor.IsTor(ip)
        else:
            tor = False

        CookedLine = {
            'name': ip.strip(),
            'asn': asn.strip(),
            'cidr': cidr.strip(),
            'country': country.strip(),
            'nir': nir.strip(),
            'date': date.strip(),
            'desc': desc.strip(),
            'size': 1,
            'tor': tor
        }
        add_ng(result, CookedLine['country'], CookedLine['cidr'], CookedLine)
    Oops = Rebuild(result)

    #pprint(result)
    #json.dumps(result, sort_keys=True, indent=4)

    Filename = "Oops.json"
    with open(Filename, 'w') as outfile:
        #json.dump(result, outfile, sort_keys=True, indent=4)
        json.dump(Oops, outfile, indent=4)
        #json.dump(result, outfile)

def ASNtoJSON(ASNlist, keyword):
    """Create a dict and Rebuild it to something JSON-ish"""
    result = {}
    print "Doing ASNtoJSON: %s" % (keyword)
    for RawLine in ASNlist:
        try:
            asn, ip, cidr, country, nir, date, desc = RawLine.split('|')
        except:
            continue

        if CheckTOR:
            tor = IsTor.IsTor(ip)
        else:
            tor = False

        CookedLine = {
            'name': ip.strip(),
            'asn': asn.strip(),
            'cidr': cidr.strip(),
            'country': country.strip(),
            'nir': nir.strip(),
            'date': date.strip(),
            'desc': desc .strip(),
            'size': 1,
            'tor': tor
        }
        add(result, CookedLine[keyword], CookedLine)
    #Oops = Rebuild(result)

    #pprint(result)
    #print json.dumps(result, sort_keys=True, indent=4)

    Filename = "%s.json" % key
    with open(Filename, 'w') as outfile:
        #json.dump(result, outfile, sort_keys=True, indent=4)
        #json.dump(Oops, outfile)
        json.dump(result, outfile)

if __name__ == "__main__":
    import argparse
    import IPsort
    import BulkWhoIs

    parser = argparse.ArgumentParser(description="Grok file....")
    parser.add_argument('file', help='File do do magic on. Produce a "<key>.json" file.')
    parser.add_argument('-t', '--tor', action="store_true", help='Check for TOR-exit node')
    parser.add_argument('-s', '--separator', type=str, help='Seperator', default=';')
    parser.add_argument('-k', '--key', type=str, help='sort key', choices=['asn', 'ip', 'cidr', 'country','all', 'special'], default='all')
    args = parser.parse_args()
    print args
    file = args.file
    sep = args.separator
    key = args.key
    CheckTOR = args.tor
    
    #print args

    print "Doing IPort on %s using '%s'" %( file, sep)
    list = IPsort.do_magic(file, sep)
    print "Doing WhoIs..."
    list = IPsort.do_magic(file, sep)
    result = BulkWhoIs.MyWhoIs(list)
    if key == 'all':
        ASNtoJSON(result, 'asn')
        ASNtoJSON(result, 'ip')
        ASNtoJSON(result, 'cidr')
        ASNtoJSON(result, 'country')
    if key == 'special':
        jason(result)
    if (key != 'all') and (key != 'special'):
        ASNtoJSON(result, key)

