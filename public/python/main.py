import os
import string
import readpdf
import time
import json

from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

os.environ['APPDATA'] = os.getcwd() + "\\python\\nltk_data"

from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
from nltk.stem import WordNetLemmatizer
from nltk.stem import PorterStemmer
import numpy as np
from scipy.linalg import norm
from sklearn.feature_extraction.text import CountVectorizer
import pandas as pd

doc = []

def print_cosinesimilarity(s1, s2):
    documents = [s1, s2]

    count_vectorizer = CountVectorizer(stop_words='english')
    count_vectorizer = CountVectorizer()
    sparse_matrix = count_vectorizer.fit_transform(documents)

    doc_term_matrix = sparse_matrix.todense()
    df = pd.DataFrame(doc_term_matrix,
                      columns=count_vectorizer.get_feature_names())
    x=cosine_similarity(df, df)
    return str(x[0][1])

def main():
#    print(calc_and_print_CosineSimilarity_for_all(s1,s2))
    cwd = os.getcwd()
    for file in os.listdir(cwd + "\\python\\Policy"):
#         if(file == "Academic Progression Mandatory Interview Procedure.pdf"):
        doc.append(os.path.splitext(file)[0])
        PDFFile = open(cwd + "\\python\\Policy\\" + file,'rb')
        readpdf.read_pdf(PDFFile, file, doc)
#    baseFolderPath = "./inputdata/"
    data = {}
    for i in readpdf.dlist:
        #print("Policy Name : " + i[0])
        #print("==================================================================")

        fileNames = []
        if (len(i[1]) > 0):
            for l in i[1]:
                rawContentDict =[]
                ind = list(filter(lambda x:x[0]==str(l+".pdf"), readpdf.dlist))
                pair = {}
                pair[str(ind[0][0])] = print_cosinesimilarity(i[2],str(ind[0][2]))
                #print(str(ind[0][0]) + " : Similarity = " + print_cosinesimilarity(i[2],str(ind[0][2])))
                fileNames.append(pair)
        #print("==================================================================")
        data[i[0]] = fileNames
    print(json.dumps(data))
main()
