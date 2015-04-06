__author__ = 'Cydal'

import json
import xml.etree.cElementTree as ET
import codecs





filename = "C:\Users\Cydal\Documents\wrangling\\hamilton_canada.osm"

dicta = {}
pretty = True
file_out = "{0}_meta.json".format(filename)
#Opening file write stream
with codecs.open(file_out, "w") as fo:
    for event, element in ET.iterparse(filename):
        ##if element is a node or a way
        if element.tag == "node" or element.tag == "way":
            tempa = []
            #timef = datetime.strptime(element.attrib["timestamp"], "%Y-%m-%dT%H:%M:%SZ")
            #timef = timef.replace(tzinfo=None).strftime("%Y-%m-%d")
            
            #Only Node tag contains lat and lon fields
            if element.tag == "node":
                temp = {element.attrib["timestamp"]: { 
                        "lat": element.attrib["lat"], 
                        "lon": element.attrib["lon"], 
                        "tag": element.tag }
                        }
            else:
                temp = {element.attrib["timestamp"]: {
                        "tag": element.tag }
            }
            
            dicta = { "username": element.attrib["user"], "other": temp}
            
            #dicta[element.attrib["user"]] = temp
            
            ##Writing to json file.
        if pretty:
            fo.write(json.dumps(dicta, indent=2)+ "\n")
        else:
            fo.write(json.dumps(dicta)+"\n")            
            '''
            if element.attrib["user"] in dicta:
                tempa.append(temp)
            else:
                dicta[element.attrib["user"]] = []
                tempa = temp
            dicta[element.attrib["user"]].append(tempa)
            '''
    
