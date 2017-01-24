try:
    import xml.etree.cElementTree as ET
except ImportError:
    import xml.etree.ElementTree as ET

#kitchen package for dealing with encoding
from kitchen.text.converters import to_unicode

import numpy as np
import pandas as pd

#my functions
from InputDataProcessing import StringCleanUp


def SaveChunkDataToFile(fileToSave, dataToSave, isFirstChunk):

     #save dataframe to csv file
     df_outputData = pd.DataFrame(data=dataToSave)
     df_outputData.to_csv(path_or_buf = fileToSave, header=isFirstChunk, index=False, encoding='utf-8')
     df_outputData = pd.DataFrame()
     print '---->>> Data Chunk Saved <<< ---'



def SaveWikiDumpToCSV(source, outFilePath, numberPagesToImport, saveChunkSize=100):

    page_name = '{http://www.mediawiki.org/xml/export-0.10/}'
    page_URI = u'https://pl.wikipedia.org/wiki/'
    page_tag = page_name + 'page'

    outputFile = open(outFilePath, 'w')

    count = 0;              #counter of registered wiki pages
    maxTextSize = 400000    #max sie of article on page

    #output numpy array -  title of page
    wikiTitle = np.chararray(numberPagesToImport, unicode=True)
    wikiTitle = np.chararray(wikiTitle.shape, itemsize=256, unicode=True)   #max size of title 256 chars
    wikiTitle[:] = u'.'

    #text
    wikiText = np.chararray(numberPagesToImport, unicode=True)
    wikiText = np.chararray(wikiText.shape, itemsize=maxTextSize, unicode=True)      #max size of title 2048 chars
    wikiText[:] = u'.'

    #output data as an array
    outputData = []

    #dictonar with output data (for one page)
    pageData = {}

    #iterate over each wiki page in dump file
    for event, page in ET.iterparse(source):

        if page.tag == page_tag and event == 'end':
        
            #iterate throuh out all elements on page
            for elem in page:

                #if the element is title put it to the array
                if elem.tag == page_name + 'title':
                        
                    #load title of page and transform it to unicode
                    u_wikiTitle = to_unicode(elem.text, 'utf-8').strip()

                    pageData['URI'] = page_URI + u_wikiTitle
                    pageData['name'] = u_wikiTitle.lower()

                #if the element is text add it to the array and increment count
                if elem.tag == page_name + 'revision':

                    #search for text tag
                    for subelem in elem:

                        if subelem.tag == page_name + 'text':

                            #load the text and transform it to unicode
                            u_wikiText = to_unicode(subelem.text, 'utf-8').strip()

                            #sometimes there is no text in wiki page
                            if u_wikiText is None:
                                u_wikiTextStr = u' '

                            #make all text in lower case
                            u_wikiText = u_wikiText.lower()

                            #clean up the text from html tags and special charaters
                            u_cleanUpText = StringCleanUp(u_wikiText)
                    
                            #check if there is enough space for page text
                            if len(u_cleanUpText) > maxTextSize:
                                s = 'Some text on page is longer than max allocated size: '
                                s = s + str(len(u_cleanUpText)) + '\n'
                                print s

                            #put the value to the dictionary
                            pageData['text'] = u_cleanUpText

            page.clear() #free the allocated mememory

            #creat array of dictionaries one for each page
            outputData.append(pageData.copy())
           
            #increment the page counter
            count +=1

            #check if there is more pages in dump file waiting to be imported
            if count > numberPagesToImport:
                print '\n'
                print 'WARNING: There is more than ' + str(numberPagesToImport) + ' pages in wiki dump file\n'
                count -= 1
                break

            #print progress
            print("Progress: {0:.2f}%".format((count * 100.0)/numberPagesToImport))

            #when chunk is full save it to csv file
            if (count % saveChunkSize) == 0:

                SaveChunkDataToFile(outputFile, outputData, count==saveChunkSize)
                
                #clear the outputData array
                outputData = []
                
            #check if the last chunk is not fully filled with data
            if (count == numberPagesToImport) and len(outputData) > 0 :
                SaveChunkDataToFile(outputFile, outputData, count<saveChunkSize)
                outputData = []

    #close the output file
    outputFile.close()
        
    print 'Total number of registered wiki pages: ' + str(count) + '\n'

