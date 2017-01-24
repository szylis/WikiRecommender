#TEST FUNCTIONS


#this will test the ordering the pages in the matrix
#this is very simple and naive test to check if the 1st and 8th page have 4 common words
def MatrixOrderTest(df_big_frame):

    first_page = df_big_frame.iloc[1]

    commonWords = (first_page * df_big_frame.iloc[8]).tolist()

    wordCount = 0
    for word in commonWords:
        if (word > 0.0):
            wordCount += 1
    
    assert wordCount == 4, 'TEST FAILED'