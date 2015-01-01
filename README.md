Plotting Paratexts
==================

This is for code related to my project on www.paratexts.org . 
The scripts are made to draw information from the TCP (Text Creation Partnership) XML-TEI files.

EEBO-TCP phase 1:
Download and extract files from
https://umich.app.box.com/s/nfdp6hz228qtbl2hwhhb to a “files”
directory. 

ECCO-tcp: Download the bibliographic header and the file batches from http://www.textcreationpartnership.org/tcp-ecco/  to a 'files' directory

Whereas EEBOtcp1 files are headed (the headers joined with the files), some of the scripts that have to run on ECCO-tcp files include a 'getheader' function that would join file and header.
============================================
Extracting dates:
Use dateinfo files. Also requires the functions in GetDateDef.py!
