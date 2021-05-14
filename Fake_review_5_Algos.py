from flask import Response
import numpy as np # linear algebra
import pandas as pd # data processing, CSV file I/O (e.g. pd.read_csv)
from sklearn.naive_bayes import MultinomialNB

import pickle
import json
import csv

import os
for dirname, _, filenames in os.walk('/kaggle/input'):
    for filename in filenames:
        print(os.path.join(dirname, filename))

# Any results you write to the current directory are saved as output.

import re
import string
from nltk.corpus import stopwords
from bs4 import BeautifulSoup
import nltk
from nltk.corpus import stopwords
from nltk.stem import SnowballStemmer
from sklearn import preprocessing 
import nltk
nltk.download('stopwords')
from sklearn.model_selection import train_test_split
from sklearn.feature_extraction.text import CountVectorizer, TfidfVectorizer
from sklearn.metrics import accuracy_score, confusion_matrix

from sklearn.model_selection import train_test_split
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.svm import SVC 
from sklearn.metrics import accuracy_score, precision_score, recall_score, f1_score
from sklearn.linear_model import SGDClassifier
from sklearn.linear_model import LogisticRegression
import statistics 
from statistics import mode 


def Algo_output_fun(sample):
  

    #sample="I've stayed at several different hotels in Chicago but The James is the best. Everything I need is in walking distance and I find it very convenient to stay there. The staff at the concierge desk is so polite and offers assistance willingly. The room has always been very clean. The bed linens are better that the nice sheets I have on my own bed. Thankfully I don't have to search around for somewhere to stay when I travel there as I've found my favorite."
    sample=clean_numbers(sample)
    sample=clean_char(sample)
    sample=clean_text(sample)

    words = {}
    with open('fake_review_word_feature_space.json', 'r') as fp:
        words = json.load(fp)

    length = len(words)
    incoming = [0] * length
    clean_words = re.sub("[^\w]", " ", sample).split()

    for i in clean_words:
        if i in words:
            index = words[i]
            incoming[index] += 1

    #print("\nNaive Bayes Output")
    naive_model = pickle.load(open('naivebayes.pkl','rb'))
    outcome1 = naive_model.predict([incoming])
    result1 = int(outcome1[0])

    #print("SVM OUTPUT")
    svm = pickle.load(open('svm.pkl','rb'))
    outcome2 = svm.predict([incoming])
    result2 = int(outcome2[0])

    #print("SGD Clf OUTPUT")
    sgd = pickle.load(open('sgd_clf.pkl','rb'))
    outcome3 = sgd.predict([incoming])
    result3 = int(outcome3[0])

    #print("Logistic regression OUTPUT")
    lr = pickle.load(open('logistic_regression.pkl','rb'))
    outcome4 = lr.predict([incoming])
    result4 = int(outcome4[0])

    #print("Decision Tree OUTPUT")
    dt = pickle.load(open('decision_tree.pkl','rb'))
    outcome5 = dt.predict([incoming])
    result5 = int(outcome5[0])

    return json.dumps(result1),json.dumps(result2),json.dumps(result3),json.dumps(result4),json.dumps(result5)    


def clean_text(text):
    
    ## Remove puncuation
    text = text.translate(string.punctuation)
    
    ## Convert words to lower case and split them
    text = text.lower().split()
    
    ## Remove stop words
    stops = set(stopwords.words("english"))
    text = [w for w in text if not w in stops and len(w) >= 3]
    
    text = " ".join(text)

    # Clean the text
    text = re.sub(r"[^A-Za-z0-9^,!.\/'+-=]", " ", text)
    text = re.sub(r"what's", "what is ", text)
    text = re.sub(r"\'s", " ", text)
    text = re.sub(r"\'ve", " have ", text)
    text = re.sub(r"n't", " not ", text)
    text = re.sub(r"i'm", "i am ", text)
    text = re.sub(r"\'re", " are ", text)
    text = re.sub(r"\'d", " would ", text)
    text = re.sub(r"\'ll", " will ", text)
    text = re.sub(r",", " ", text)
    text = re.sub(r"\.", " ", text)
    text = re.sub(r"!", " ! ", text)
    text = re.sub(r"\/", " ", text)
    text = re.sub(r"\^", " ^ ", text)
    text = re.sub(r"\+", " + ", text)
    text = re.sub(r"\-", " - ", text)
    text = re.sub(r"\=", " = ", text)
    text = re.sub(r"'", " ", text)
    text = re.sub(r"(\d+)(k)", r"\g<1>000", text)
    text = re.sub(r":", " : ", text)
    text = re.sub(r" e g ", " eg ", text)
    text = re.sub(r" b g ", " bg ", text)
    text = re.sub(r" u s ", " american ", text)
    text = re.sub(r"\0s", "0", text)
    text = re.sub(r" 9 11 ", "911", text)
    text = re.sub(r"e - mail", "email", text)
    text = re.sub(r"j k", "jk", text)
    text = re.sub(r"\s{2,}", " ", text)
    
    text = text.split()
    stemmer = SnowballStemmer('english')
    stemmed_words = [stemmer.stem(word) for word in text]
    text = " ".join(stemmed_words)

    return text

def clean_char(x):

    puncts = [',', '.', '"', ':', ')', '(', '-', '!', '?', '|', ';', "'", '$', '&', '/', '[', ']', '>', '%', '=', '#', '*', '+', '\\', '•',  '~', '@', '£', 
    '·', '_', '{', '}', '©', '^', '®', '`',  '<', '→', '°', '€', '™', '›',  '♥', '←', '×', '§', '″', '′', 'Â', '█', '½', 'à', '…', 
    '“', '★', '”', '–', '●', 'â', '►', '−', '¢', '²', '¬', '░', '¶', '↑', '±', '¿', '▾', '═', '¦', '║', '―', '¥', '▓', '—', '‹', '─', 
    '▒', '：', '¼', '⊕', '▼', '▪', '†', '■', '’', '▀', '¨', '▄', '♫', '☆', 'é', '¯', '♦', '¤', '▲', 'è', '¸', '¾', 'Ã', '⋅', '‘', '∞', 
    '∙', '）', '↓', '、', '│', '（', '»', '，', '♪', '╩', '╚', '³', '・', '╦', '╣', '╔', '╗', '▬', '❤', 'ï', 'Ø', '¹', '≤', '‡', '√', ]

    x = str(x)
    for punct in puncts:
        if punct in x:
            x = x.replace(punct, f' {punct} ')
    return x

def clean_numbers(x):
    if bool(re.search(r'\d', x)):
        x = re.sub('[0-9]{5,}', '#####', x)
        x = re.sub('[0-9]{4}', '####', x)
        x = re.sub('[0-9]{3}', '###', x)
        x = re.sub('[0-9]{2}', '##', x)
    return x


def mlmodels_2():

    result=list()
    fresult=list()
    maxvote=list()
    with open('Hotelreview_testingData.csv', newline='') as csvfile:
        data = csv.DictReader(csvfile)
        for row in data:
            result.append(row['Reviews'])

    for i in range(len(result)):
        reviews=result[i]
        fresult.append(Algo_output_fun(reviews))

    for i in range(len(fresult)):
        list_no1 = fresult[i]
        maxvote.append(mode(list_no1))


    indata = pd.read_csv('Hotelreview_testingData.csv')
    zipped = pd.DataFrame(fresult)
    Mvote=pd.DataFrame(maxvote)
    '''print(zipped)
    print(indata)
    print(Mvote)'''

    #axis=1 indicates to concat the frames column wise
    outdata = pd.concat([indata, zipped,Mvote], axis=1)
    #we dont want headers and dont want the row labels
    outdata.to_csv('fake_review_out.csv', header=False, index=False)
    foutput=pd.read_csv("fake_review_out.csv",sep=",",names=["ReviewID","Review", "Hotel", "City","UserName","Naive_Bayes T=1/D=0","SVM T=1/D=0","SGD_CLF T=1/D=0","Logistic_Regression T=1/D=0","Decision_Tree T=1/D=0","Final Output T=1/D=0"])
    #print(foutput)
    foutput.to_csv('fake_review_out.csv', index=False)


