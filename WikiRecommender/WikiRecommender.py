import locale
import os
import sys

import pandas as pd

#kitchen package for dealing with encoding
from kitchen.text.converters import getwriter, to_unicode, to_bytes
from kitchen.i18n import get_translation_object

#importing my additionally functions
from InputDataProcessing import *
from ImportWikiDump import *
from TextAlgorithms import *


#encoding - dealing with text -  seting up the stdout
encoding = locale.getpreferredencoding()
writer = getwriter(encoding)
sys.stdout = writer(sys.stdout) #it will convert unicode string to ascii when send to stdout - terminal

## ---- CONTROL FLAGS

saveWikiData = True # save clean wiki data on disk as a csv file

loadCorpusData = False

## -----

#wikipedia dump xml to csv file
if(saveWikiData):
    SaveWikiDumpToCSV('PLWiki/PLwiki.xml', '.\Output\PLWiki_DF.csv', 100, 50)


#read data from csv file
wikiDataFile = open('.\Output\PLWiki_DF.csv', 'r+')
df_wikiData = pd.read_csv(filepath_or_buffer = wikiDataFile, encoding='utf-8')

#count the word and create an array of dictionaries with word count
df_wikiData = CountWords(df_wikiData)



if(not(loadCorpusData)):

    #creat a spares matrix with whole corpus
    #row (index) - single word
    #column - wiki page
    #value - (word count)
    df_CorpusData = CorpusCountWords(df_wikiData)

    #if data are big it might be worth to save it
    df_CorpusData.to_pickle('.\Output\CorpusData')

else:
    df_CorpusData = pd.read_pickle('.\Output\CorpusData')


quarryPage = 42

NN = FindNearestNeighbor(df_CorpusData, quarryPage, 5)


print '--------------------------------------'
print 'QUARRY: ' + df_wikiData['name'][quarryPage]
#print df_wikiData['URI'][quarryPage]
print '--------------------------------------'
print '--------------------------------------'

for i in range(len(NN)):
    print str(i) + '-NEAREST: ' + df_wikiData['name'][NN[i]]

#print df_wikiData['URI'][NN]
print '--------------------------------------'
#print '\n'
#print 'TEXT:'
#print '--------------------------------------'
#print df_wikiData['text'][quarryPage]
#print '\n'
#print 'WORD COUNT'
#print '--------------------------------------'
#print df_wikiData['word count'][quarryPage]

wikiDataFile.close()