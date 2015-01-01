#!/usr/bin/env python3
# -*- coding: utf-8 -*-

ROOT_PATH = 'files'

import os, time
import xml.etree.ElementTree as ET
from GetDateDef import get_year, todecades

text_fn ="dateinfo_%s" % time.strftime('%Y%m%d_%H%M%S')
text_file = open(text_fn + '.txt', 'w')

def process_text(doc_id, input_el):
    title = input_el.find('FILEDESC/TITLESTMT/TITLE')    
    title_date = input_el.find('FILEDESC/SOURCEDESC/BIBLFULL/PUBLICATIONSTMT/DATE')    
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
    
    for input_el in input_root.findall('HEADER'):
        process_text(doc_id, input_el)

##########

import argparse

parser = argparse.ArgumentParser(description='Analyze the paratexts in historical texts')
parser.add_argument('--dir', default=ROOT_PATH, help='Directory of XMLs')

args = parser.parse_args()

for dirpath, dirs, files in os.walk(args.dir):
    for fname in files:
            doc_id = os.path.splitext(fname)[0]
            process_xml(doc_id, os.path.join(dirpath, fname))