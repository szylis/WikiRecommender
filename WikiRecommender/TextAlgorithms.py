import pandas as pd
import numpy as np
from math import sqrt

#imput data are dictionary with word as a kay and numeric value
def EuclideanDistance(query, page):

     x = query - page
     x = np.transpose(x) * x
     
     return sqrt(sum(x))
    
   
def NearestNeighbor(model, query, k=1):

    distances = [float("inf")] * k
    nearests = [query] * k

    numberOfPages = (model.shape)[0]
    querPage = np.array((model.todense())[query, :]).flatten()

    #iterate over all pages and count the distance
    for i in range(numberOfPages):

        if(i%50 == 0):
            print 'Progress: ' + str(i*100.0/numberOfPages) + '%'

        #comput the distance between query page and pages in library       
        if (i != query):

            temp_dist = EuclideanDistance(querPage, np.array((model.todense())[i, :]).flatten())

            #check if the new distance to smaller than the istance to the last element in the list
            if (temp_dist < distances[-1]):
                nearests[-1] = i
                distances[-1] = temp_dist

                #and sort in reference to the distance

                zipped = zip(distances, nearests)   #first zip the distance and nearest
                zipped = sorted(zipped)             #sort
                distances, nearests = zip(*zipped)  #and unzip

                distances = list(distances)
                nearests = list(nearests)

    #return index of the nearest neighbor
    return nearests