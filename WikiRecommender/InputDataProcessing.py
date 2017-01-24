import re
import time
import pandas as pd

from TestFunctions import *



#function for cleaning the wiki page
def StringCleanUp(s):

    #remove the #REDIRECT word from text
    s = re.sub(r'#.*? ', ' ', s) 
    
    #html table tags
    s = re.sub(r'class=".*?"', ' ', s)
    s = re.sub(r'style=".*?"', ' ', s)
    s = re.sub(r'scope=".*?"', ' ', s)
    s = re.sub(r'rowspan=".*?"', ' ', s)
    s = re.sub(r'colspan=".*?"', ' ', s)

    s = re.sub(r'<br>', ' ', s)
        
    s = re.sub(r'<ref .*?</ref>', ' ', s) #remove the HTML TAG <REF> </REF>
    s = re.sub(r'<ref>.*?</ref>', ' ', s) #remove the HTML TAG <REF> </REF>
    s = re.sub(r'<code>.*?</code>', ' ', s)
    s = re.sub(r'<math>.*?</math>', ' ', s)
    s = re.sub(r'http://.*? ', ' ', s)
    s = re.sub(r'&nbsp', ' ', s)
    s = re.sub(r'<small>', ' ', s)
    s = re.sub(r'</small>', ' ', s)
    s = re.sub(r'<br />', ' ', s)
    s = re.sub(r'<sup>', ' ', s)
    s = re.sub(r'</sup>', ' ', s)
    s = re.sub(r'<sub>', ' ', s)
    s = re.sub(r'</sub>', ' ', s)
    s = re.sub(r'</blockquote>', ' ', s)
    s = re.sub(r'</syntaxhighlight>', ' ', s)
    
    #file on the page
    s = re.sub(r'thumb', ' ', s)
    s = re.sub(r'.com', ' ', s)
    s = re.sub(r'.jpg', ' ', s)
    s = re.sub(r'.png', ' ', s)
    s = re.sub(r'.svg', ' ', s)
    
    #single charater
    s = re.sub(r' . ', ' ', s)


    chars_to_remove = ["[", "]", "'", "=", ',', '.', ':', '"', '*', '(', ')', '{', '}', '|', ';', '-', '%', '0', '1', '2', '3', '4', '5', '6', '7', '8', '9']

    for char in chars_to_remove:
        s = s.replace(char, ' ')

    s = re.sub(r'\n', ' ', s)
    s = re.sub(' +', ' ', s) #remove multiple space char
    

    return s

#function counting word occurrence on the page
def CountWords(df_inputData):

    wordsCount = {} #dictionar for word count 
    tempWordCount = [] #creat temp array for word count

    #loop over all pages
    for k in range (len(df_inputData.index)):
        
        # check if there is text field in dictionary
        if 'text' in df_inputData.columns:

            words = df_inputData['text'][k].split()

            #each unique word is a key in dictionary - value represent occurrence of this word in text
            for word in words:

                #check if dictionary has already this word
                    if word in wordsCount.keys():
                        wordsCount[word] += 1       #yes, so increment value
                    else:
                        wordsCount[word] = 1        #no, so put 1 as a value

        else:
            print 'WARNING: -Text- key is missing in dictionary'
        
        #add current word count to the temp array
        tempWordCount.append(wordsCount.copy())

        #clear the list of word count before next iteration
        wordsCount.clear()
    
    df_inputData['word count'] = tempWordCount

    return df_inputData


#transforming the word count column to a new dataframe with (page_id, feature_id, word_count)
def StackWordCount(df_corpus):

    #loop over whole corpus
    for pageIndex in range(len(df_corpus)):

        if (pageIndex == 0):
            x = df_corpus.iloc[pageIndex]['word count']
            x = pd.DataFrame(x.items(), columns=['feature', 'value'])
            x['id'] = pageIndex

        else:
            y = df_corpus.iloc[pageIndex]['word count']
            y = pd.DataFrame(y.items(), columns=['feature', 'value'])
            y['id'] = pageIndex

            #add to the existing dataframe
            x = x.append(y, ignore_index=True)

    return x

#function which creates a big sparse matrix with whole corpus words count
def CorpusCountWords(df_corpus):

    #loop over whole corpus
    for pageIndex in range(len(df_corpus)):
        
        #first element is starting the matrix
        if (pageIndex == 0):
            frame = pd.DataFrame(data=df_corpus['word count'][pageIndex], index=[pageIndex])

        #other elements need to be concetrated with the previous matrix
        else:
            df_temp = pd.DataFrame(data=df_corpus['word count'][pageIndex], index=[pageIndex])
            frame = pd.concat([frame, df_temp])

    #fill NaN to 0.0
    frame = frame.fillna(0)

    #HEALTH TEST - 1 and 8 pages have 4 common words
    if (len(frame) > 8):
        MatrixOrderTest(frame)

    #DataFrame to sparse matrix
    #**sparse matrix is optimized to deal with row-wise matrix 
    # as a page number is smaller than word number let's transpose data
    frame = pd.DataFrame.transpose(frame)

    #it can take a moment or two
    start=time.time()
    frame = frame.to_sparse(fill_value=0)
    end=time.time()

    print 'Conversion to sparse matrix time: ' + str(end-start) + '\n'
    print 'Density of sparse matrix: ' + str(frame.density) + '\n'

    return frame
    







    

    