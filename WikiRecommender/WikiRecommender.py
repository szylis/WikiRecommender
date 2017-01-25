import locale
import os
import sys
import time

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
    SaveWikiDumpToCSV('PLWiki/PLwiki.xml', '.\Output\PLWiki_DF.csv', 1000, 50)

#read data from csv file
wikiDataFile = open('.\Output\PLWiki_DF.csv', 'r+')
df_wikiData = pd.read_csv(filepath_or_buffer = wikiDataFile, encoding='utf-8')

#add word count to the data matrix
#word count represent a count of words in each page 
#output: an input array plus a new column ['word count'] which contains a dictionary  (key -> word, value -> word count)
#start = time.time()
#df_wikiData = CountWords(df_wikiData)
#end = time.time()

#print 'Word count for each page -> time: ' + str(end - start) + 's'

#translate the text to vector space
#output:
# data matrix with word count - PxF, where P - wiki pages, F - featers words 
# mapping the words with coded index 
start = time.time()
sm_WordCount, mapping = VectorizeText(df_wikiData)
end = time.time()

print 'Text into vector space -> time: ' + str(end - start) + 's'


#find the tf-idf for documents in corpus
#input: the sparse matrix with word count
#output: sparse matrix with tf-idf values
start = time.time()
sm_tfidf = TF_IDF_smatrix(sm_WordCount)
end = time.time()

print 'TF-IDF for each page -> time: ' + str(end - start) + 's'


queryPage = 173

start = time.time()
NN = NearestNeighbor(sm_tfidf, queryPage, 5)
end = time.time()

print 'kNearestNeighbor algorythm time: ' + str(end - start)


print '--------------------------------------'
print 'QUERY: ' + df_wikiData['name'][queryPage]
print df_wikiData['URI'][queryPage]
print '--------------------------------------'
print '--------------------------------------'

for i in range(len(NN)):
    print str(i) + '-NEAREST: ' + df_wikiData['name'][NN[i]]

wikiDataFile.close()