#!/usr/bin/env python3
# -*- coding: utf-8 -*-

ROOT_PATH = 'files'

import os, time
import xml.etree.ElementTree as ET
from GetDateDef import get_year, todecades

text_fn ="ECCOdateinfo_%s" % time.strftime('%Y%m%d_%H%M%S')
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

import argparse

parser = argparse.ArgumentParser(description='Analyze the paratexts in historical texts')
parser.add_argument('--dir', default=ROOT_PATH, help='Directory of XMLs')

args = parser.parse_args()

output_root = ET.Element('PARATEXTS')
output_tree = ET.ElementTree(output_root)

paratext_type_dict = {}

for dirpath, dirs, files in os.walk(args.dir):
    for fname in files:
            doc_id = os.path.splitext(fname)[0]
            process_xml(doc_id, os.path.join(dirpath, fname))
