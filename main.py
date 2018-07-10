# -*- coding: utf-8 -*-
"""
Created on Wed Feb 03 08:14:58 2018

@author: Suresh Kumar Tathari

main body
"""
# importing regular expression
import re

# importing the required functions file
import Acronymfunctions as af

# Reading the text file might cause I/O operation
try:
    words = []  # list of words in a text file
    with open('text.txt', 'r') as content_file:
        content = content_file.read()  # for reading a file with multiple lines
        # print content
        words = content.split()

    # getting capital words of length >=3 and length <10
    capitalwords = [x for x in words if (x.isupper() and len(x) >= 3 and len(x) < 10)]

    # Checking and Removing braces if present
    capitalwordsnospc = re.findall('[\w]+', ''.join(capitalwords))

    # Acronym list by definition of length >=3 and <10
    acronymList = [x for x in capitalwordsnospc if (x.isupper() and len(x) >= 3 and len(x) < 10)]
    # print capitalwords
    # print acronymList

    # acronym dictionary
    acronym_dictionary = {}

    for acronym in acronymList:
        af.get_Acronym_Definition(words, acronym)
        acronym_dictionary[acronym] = af.get_Acronym_Definition(words, acronym)

    print "Acronyms and its defintions"
    
    print acronym_dictionary

except Exception as e:
    print e
