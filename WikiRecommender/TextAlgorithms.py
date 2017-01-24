import pandas as pd
from math import sqrt

#imput data are dictionary with word as a kay and numeric value
def EuclideanDistance(quarry, page):

     x = (quarry - page)
     x = pd.Series.transpose(x) * x
     
     return sqrt(sum(x))
    


    
    

    
def FindNearestNeighbor(df_WikiCorpus, quarry, k=1):

    distances = [float("inf")] * k
    nearests = [quarry] * k

    #iterate over all pages and count the distance
    for i in range(len(df_WikiCorpus.columns)):
        
        #comput the distance between quarry page and pages in library       
        if (i != quarry):
        
            temp_dist = EuclideanDistance(df_WikiCorpus[quarry], df_WikiCorpus[i])

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