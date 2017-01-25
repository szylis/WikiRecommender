import re
import time
import pandas as pd

from math import log1p
from TestFunctions import *

# Machine Learning in Python
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.feature_extraction.text import TfidfTransformer


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
#adding new column ['word count'] which contains dictionary (key -> word, value -> word count in page)
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



#pass a element which you want to find,
#and map to decode the value of element 
def FindElementValue(elem, values, map):
  
     try: 
        return values[0, map.index(elem)]

     except ValueError:
        return 0

#function counting word occurrence on the page
#adding new column ['word count'] which contains dictionary (key -> word, value -> word count in page)
#this version is using a scikit for text
def NewCountWords(df_inputData):
    
    wordsCount = {} #dictionar for word count 
    tempWordCount = [] #creat temp array for word count

    # check if there is text field in dictionary
    if 'text' not in df_inputData.columns:
        print 'ERROR: not text to work with'
        return

    #instance of Count Vectorizer
    vectorizer = CountVectorizer()

    #translate the text to vector space
    #output data matrix with word count
    # PxF, where P - wiki pages, F - featers words  

    #I use fit_transform method on whole carpus. In the future I can split corpus for train and test set
    #then I will use train set for finding the stop words and for build a model
    #then using model I can analyse the whole corpus using transform method  
    data = vectorizer.fit_transform((df_inputData['text']).tolist())

    #list with all words, correspond to the value in data matrix
    mapping = vectorizer.get_feature_names()

    #loop over all pages
    for k in range (len(df_inputData.index)):

        #creat list of words from page text
        words = df_inputData['text'][k].split()

        #get the word count for k-th page - row access in data matrix
        page_data = ((data.todense())[k,:])
      
        #each unique word is a key in dictionary - value represent occurrence of this word in text
        for word in words:

            #add word to dictionary 
            #this is not efficient for long size text          
            wordsCount[word] = FindElementValue(word, page_data, mapping)  
               
        #add current word count to the temp array
        tempWordCount.append(wordsCount.copy())

        #clear the list of word count before next iteration
        wordsCount.clear()
    
    #creat a new column for word count
    df_inputData['word count'] = tempWordCount

    return df_inputData


#translate the text to vector space
#output:
# data matrix with word count - PxF, where P - wiki pages, F - featers words 
# mapping the words with coded index
def VectorizeText(df_inputData):

    # check if there is text field in dictionary
    if 'text' not in df_inputData.columns:
        print 'ERROR: not text to work with'
        return

    #instance of Count Vectorizer
    vectorizer = CountVectorizer()

    #translate the text to vector space
    #output data matrix with word count
    # PxF, where P - wiki pages, F - featers words  

    #I use fit_transform method on whole carpus. In the future I can split corpus for train and test set
    #then I will use train set for finding the stop words and for build a model
    #then using model I can analyse the whole corpus using transform method  
    data = vectorizer.fit_transform((df_inputData['text']).tolist())

    #list with all words, correspond to the value in data matrix
    mapping = vectorizer.get_feature_names()

    return data, mapping



def TF_IDF_smatrix(word_count):

    tfidf = TfidfTransformer(norm="l2")

    tfidf.fit(word_count)
    # print "IDF: ", tfidf.idf
        
    tfidf_smatrix = tfidf.transform(word_count)

    return tfidf_smatrix



#function counting tf-idf for word on the page
#adding new column ['tf-idf'] wihich contains dictionary (key - > word, value -> tf-idf for word in the page)
def TF_IDF(df_inputData):

    #creat temp array for tf-idf
    temp_TF_IDF = [] 

    #numbre of pages in whole corpus
    totalNumberOfPages = len(df_inputData.index)

    #loop over all pages
    for k in range (totalNumberOfPages):
             
        # check if there is text field in dictionary
        if 'text' in df_inputData.columns and 'word count' in df_inputData.columns:

            # 1) first find the TF - term frequency
            #    TF = (Number of times word appears in a document) / (Total number of words in the document).

            # split text to the words
            words = df_inputData['text'][k].split() 

            # total number of words in the document
            totalNumberOfWords = len(words) 

            # make a copy of word count dictionary for single page
            temp_dict = df_inputData['word count'][k].copy()

            #interate through each key (word) in dictionary and compute the term frequency
            for key, value in temp_dict.items():

                # 2) second find the IDF - invers document frequency
                #   IDF = log_e(Total number of documents / Number of documents with word in it).

                # Number of documents with word in it
                numberOfDocuments = 0

                #loop over all page in corpus and find how many documents has searching word in it
                for p in range (totalNumberOfPages):

                    #check if page has this word
                    if df_inputData['word count'][p].has_key(key):
                        numberOfDocuments += 1       #yes, so increment value

                #compute the tf-idf
                temp_dict[key] = ((float(value))/totalNumberOfWords) / (log1p((float(totalNumberOfPages))/numberOfDocuments))


            #add current tf dict to the temp tf-idf array
            temp_TF_IDF.append(temp_dict.copy())
            
            #clear the list of tf before next iteration
            temp_dict.clear()
    
    #creat a new column for tf-idf
    df_inputData['tf-idf'] = temp_TF_IDF

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
#Creating 2D matrix (row -> page id; column -> word; value -> word count of the word in the page) 
#matrix contain all word in the corpus
def CorpusCountWords(df_corpus):


    start = time.time()

    #loop over whole corpus
    for pageIndex in range(len(df_corpus)):
        
        #first element is starting the matrix
        if (pageIndex == 0):
            frame = pd.DataFrame(data=df_corpus['word count'][pageIndex], index=[pageIndex])

        #other elements need to be concetrated with the previous matrix
        else:
            df_temp = pd.DataFrame(data=df_corpus['word count'][pageIndex], index=[pageIndex])
            frame = pd.concat([frame, df_temp])


    end = time.time()
    print 'Creating 2D matric for all pages, creation time :' + str(end-start)

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
    







    

    