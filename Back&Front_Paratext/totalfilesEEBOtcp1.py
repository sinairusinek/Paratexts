#!/usr/bin/env python3
# -*- coding: utf-8 -*-

ROOT_PATH = 'files'

# in order to find out the number of files per decade for a corpus(ECCO/EEBO-TCP), 
#and specify if they have paratext in the front, back, both or none in order to find their number and percentage(out of total of files), 
#this script outputs into the text_file in each line the filename, cleaned year, and state of paratext (frontonly, backonly, both or none)
#this will also enable to check the per-decade or annual relation of paratexts per text
#*counts only the files with clear and exact year

#########

import os, time
import xml.etree.ElementTree as ET
from GetDateDef import get_year, todecades


text_fn ="text_%s" % time.strftime('%Y%m%d_%H%M%S')
text_file = open(text_fn + '.txt', 'w')


def process_text(doc_id, input_root, text_el):
    #print('Handling ' + doc_id)
    title_date = input_root.find('HEADER/FILEDESC/SOURCEDESC/BIBLFULL/PUBLICATIONSTMT/DATE')    
    if title_date is not None: 
        year = get_year(title_date.text)
        decade = todecades(year)
        
    front_general = input_root.findall('.EEBO/TEXT/FRONT')#add non-ttl
    back_element = input_root.findall('.EEBO/TEXT/BACK')

    if title_date is not None:
        if year > 0: 
            if (front_general !=[]) and (back_element !=[]):
                coverstate= "both"
            elif front_general !=[]:
                coverstate= "frontonly"
            elif back_element !=[]:
                coverstate= "backonly"
            else:
                coverstate= "none"
            text_file.write('%-30s\t%s\t%d\t%d\n'  %(doc_id ,coverstate, year, decade))

    
def process_xml(doc_id, fname):
    try:
        input_tree = ET.parse(fname)
    except ET.ParseError:
        print ('Skipping '+ fname)
        return
    input_root = input_tree.getroot()
    file_el = ET.SubElement(output_root, 'FILE', FILENAME=fname)    
    process_text(doc_id, input_root, file_el)
    print("processing", doc_id)

##########

import argparse

parser = argparse.ArgumentParser(description='Analyze the paratexts in historical texts')
parser.add_argument('--dir', default=ROOT_PATH, help='Directory of XMLs')
parser.add_argument('--body', action='store_true', help='Include the body of paratext elements')
parser.add_argument('--full', action='store_true', help='Include the body of the document itself')

args = parser.parse_args()

output_root = ET.Element('PARATEXTS')
output_tree = ET.ElementTree(output_root)

paratext_type_dict = {}

for dirpath, dirs, files in os.walk(args.dir):
    for fname in files:
        if not fname.startswith('output') and fname.endswith(".xml"):        
            doc_id = os.path.splitext(fname)[0]
            process_xml(doc_id, os.path.join(dirpath, fname))


#import matplotlib.pyplot as pyplot
#items = [x for x in paratext_type_dict.items() if len(x[1]) > 7]

#if items:
 #   pyplot.hist([x[1] for x in items], bins=range(1600,1800,10), histtype='barstacked')
  #  pyplot.legend([x[0] for x in items])
   # pyplot.show()