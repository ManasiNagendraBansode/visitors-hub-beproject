import numpy as np
import pandas as pd
import json
import pickle
import re
from nltk.corpus import stopwords
from nltk.stem.porter import PorterStemmer

class ReviewClassifierService:

    words = {}

    model = pickle.load(open('reviewClassifier.pkl','rb'))

    def __init__(self):
        with open('word_feature_space.json', 'r') as fp:
            self.words = json.load(fp)

    #clean review get word roots, lowercase, split them by words and etc.
    def clean_review(self, review):
        review = review.lower()
        review = review.split()

        ps = PorterStemmer()

        review = [ps.stem(word) for word in review
                    if not word in set(stopwords.words('english'))]

        review = ' '.join(review)

        return review

    #return if the review was positive or negative as JSON.
    def classify(self, review):
        length = len(self.words)
        incoming = [0] * length
        clean_sample = self.clean_review(review)
        clean_words = re.sub("[^\w]", " ", clean_sample).split()

        for i in clean_words:
            if i in self.words:
                index = self.words[i]
                incoming[index] += 1

        outcome = self.model.predict([incoming])

        result = int(outcome[0])

        return json.dumps(result)