WikiPage-Recommender

Wikipedia Page Recommender is a Python script using a machine learning techniques for retrieval the most similar wiki page to query article (query does not need to be a wiki page)
The project was started in December 2016 by Szymon Lis. Project is still in early stage of development.


Installation

Dependencies

Python (>= 2.7) [It might aslo work with Ptython >= 3.3]
NumPy (>= 1.6.1)
Pandas (0.18.1)
Kitchen (1.2.4)
ElementTree (1.0.1)
  
User installation

Script needs a wikipedia dump file in xml format. You can download it from: https://en.wikipedia.org/wiki/Wikipedia:Database_download
Install all dependenices berfore starting the script.

Communication

Autor: Szymon Lis szymonlis@yahoo.com


Realse

24/01/2017
	
 - k-nearest neighbor algorithm
 - euclidean distance metric
 - word count
	
Issues

For big data transformation into sparse matrix takes huge amount of time and I'm currently working on speeding up this process. There is possibility to store precumpoute data on disk to avoid heavy computation. Also k-nearest neighbor works really.