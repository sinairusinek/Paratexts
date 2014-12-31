#!/usr/bin/env python3
# -*- coding: utf-8 -*-

ROOT_PATH = 'files'
#need to also calculate the same, but with frontext not including title pages

# in order to find out the number of files per decade for a corpus(ECCO/EEBO-TCP), 
#and specify if they have paratext in the front, back, both or none in order to fnd their number and percentage(out of total of files), 
#this script outputs into the text_file in each line the filename, cleaned year, and state of paratext (frontonly, backonly, both or none)
#this will also enable to check the per-decade or annual relation of paratexts per text
#*counts only the files with clear and exact year
#the output into the out_file will enable to report all the inexact or unclear dates, and calculate their precentage against the total/clear and vs the exact dated files
#remaining problem: I cannot make it write into the files!
#########

import os, re, time
import xml.etree.ElementTree as ET
from GetDateDef import get_year, todecades

#out_fn = "output_%s" % time.strftime('%Y%m%d_%H%M%S')
#out_file = open(out_fn + '.txt', 'w')
text_fn ="Generalinfo_%s" % time.strftime('%Y%m%d_%H%M%S')
text_file = open(text_fn + '.txt', 'w')

def get_header(doc_id):
    path = os.path.join('headers', doc_id + '.hdr')
    if not os.path.exists(path):
        return None
    tree = ET.parse(path)
    return tree.getroot()

def process_text(doc_id, input_el, text_el):
    header_el = get_header(doc_id)
    if header_el is None: 
        print ('No header for %s' % doc_id)
        return

    title = header_el.find('FILEDESC/TITLESTMT/TITLE')    
    title_date = header_el.find('FILEDESC/SOURCEDESC/BIBLFULL/PUBLICATIONSTMT/DATE')    
    if title_date is not None: 
        year = get_year(title_date.text)
        decade = todecades(year)
        text_file.write('%s\t%s\t%s\t%s\t%s\n'  %(doc_id , title.text, title_date.text, year, decade))

    
def process_xml(doc_id, fname):
    try:
        input_tree = ET.parse(fname)
    except ET.ParseError:
        print ('Skipping '+ fname)
        return
    input_root = input_tree.getroot()
    file_el = ET.SubElement(output_root, 'FILE', FILENAME=fname)
    
    for input_el in input_root.findall('EEBO/TEXT'):
        process_text(doc_id, input_el, file_el)

##########

import sys, argparse
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