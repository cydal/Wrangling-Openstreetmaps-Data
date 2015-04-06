__author__ = 'Cydal'

import re
import json
import codecs
import xml.etree.cElementTree as ET
import pprint

#Re matches, alt - street abbreviation
streettype = re.compile(r'\s(\w+\W?)$', re.IGNORECASE)
alt = re.compile(r'\b(\w*)\.$')
postcode = re.compile(r'[a-z][0-9][a-z]\s[0-9][a-z][0-9]', re.IGNORECASE)
lower = re.compile(r'^([a-z]|_)*$')
lower_colon = re.compile(r'^([a-z]|_)*:([a-z]|_)*$')
problemchars = re.compile(r'[=\+/&<>;\'"\?%#$@\,\. \t\r\n]')

mapping = {"Rd": "Road", "E.": "East", "St.": "Street"}
filename = "C:\Users\Cydal\Documents\wrangling\\hamilton_canada.osm"

#This audits and cleans the post code
def processPostCode(tag):
    m = postcode.match(tag.attrib['v'])
    if m:
        sortedpc = tag.attrib['v']
    else:
        if len(tag.attrib['v']) == 6:
            sortedpc = tag.attrib['v'][:3] + " " + tag.attrib['v'][3:]
        else:
            #Splitting the post codes that match this pattern 
            #and then recombining the disparate parts
            temp = tag.attrib['v'].strip().split(" ")
            sortedpc = temp[1] + " " + temp[2]
    return sortedpc

#This audits and cleans the address
def processAddress(tag):
    sortedadd = ""
    m = alt.search(tag.attrib['v'])
    if m:
        if m.group() in mapping.keys():
            #replacing regex match
            sortedadd = alt.sub(mapping[m.group()], tag.attrib['v'])
            return sortedadd
    else:
        return tag.attrib['v']



def processmap(element):
    dicta = {}
    #Gets tags with node or way
    if element.tag == "node" or element.tag == "way":
        #Start of data modelling
        dicta = {"id": element.attrib['id'],
                 "type": element.tag,
                 "created": {"changeset": element.attrib["changeset"],
                             "user": element.attrib["user"],
                             "version": element.attrib["version"],
                             "uid": element.attrib["uid"],
                             "timestamp": element.attrib["timestamp"]
                 }
        }
        for tag in element.iter("tag"):
            if "k" in tag.attrib.keys():
                #skip problematic chars
                if problemchars.match(tag.attrib['v']):
                    continue
                tag_key = tag.attrib['k']
                if tag_key == "address":
                    dicta["address"] = processAddress(tag)
                if tag_key == "addr:postcode":
                    returnedPCTag = processPostCode(tag)
                    dicta['postcode'] = returnedPCTag
                if tag_key == "addr:street":
                    returnedAddtag = processAddress(tag)
                    dicta["street"] = returnedAddtag
                if tag.attrib['k'] == "addr:housenumber":
                    dicta["housenumber"] = tag.attrib['v']
                if tag.attrib['k'] == "building":
                    dicta["buildingtype"] = tag.attrib['v']
        #only the node tag has the lat & lon attributes
        if element.tag == "node":
            dicta["pos"]= [float(element.attrib['lat']), float(element.attrib['lon'])]
        #if visible is present in current element
        if "visible" in element.attrib.keys():
            dicta["visible"] = element.attrib["visible"]
        #Adding nd tag
        for bag in element.iter("nd"):
            if not "node_refs" in dicta.keys():
                dicta["node_refs"] = []
            dicta["node_refs"].append(bag.attrib["ref"])
        return dicta
    else:
        return None

'''
def processdata(filename):
    
    for event, element in ET.iterparse(filename):
        returned = processmap(element)
        if returned:
            pprint.pprint(returned)
    '''
def processdata(filename, pretty=False):
    file_out = "{0}.json".format(filename)
    data = []
    #Opening filestream to save as json file
    with codecs.open(file_out, "w") as fo:
        for event, element in ET.iterparse(filename):
            returned = processmap(element)
            if returned:
                data.append(returned)
                if pretty:
                    fo.write(json.dumps(returned, indent=2)+ "\n")
                else:
                    fo.write(json.dumps(returned)+"\n")

if __name__ == "__main__":
    processdata(filename)

#db.projects.aggregate([{}])
