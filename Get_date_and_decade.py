#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# some further coding can be done here:
#can check if twice and a==b return
#have to also exclude "after/not after x" and check in EEBO "later","earlier", "before"   
#in ECCO there are two "--1798--"s which are misidentified as "range"

import re, math

YEAR_RE = re.compile(r'\d{4}')
YEARquestion_RE = re.compile(r'\d{4}\?')  
YEARange_RE = re.compile(r'\d{4}-|\/')
YEARange2_RE = re.compile(r'(\d{4}).+(\d{4})')#???
#YEARange_RE = re.compile(r'(\d{4}(-|\\)|(\d{4}){2})')

def get_year(year_text):
    match = YEAR_RE.search(year_text)
    yearange = YEARange_RE.search(year_text) 
    yearange2 = YEARange2_RE.search(year_text) 
    yearquest = YEARquestion_RE.search(year_text)

    
    if yearange2:
        return 2    #so 2 means that two dates were given as alternatives, or range. You might chose to examine those manually
    elif yearange:
        return 3    #3 means a range of years were given
    elif yearquest:
        return 0    #0 is when the date was marked with a question mark
    elif match:
        return int(match.group())
    else: 	
        return 4   # other forms of expressing uncertainty or inexactness
        
    
def todecades(intyear):
    return (intyear//10) * 10

#############  trial #############

       
def main ():
    print(get_year("1942 to 1943"))
    print(get_year("1942-43"))
    print(get_year("1942?"))
    print(get_year("1942"))
    
    print(todecades(1987))
    print(todecades(3))

if __name__=="__main__":
    main()
    
