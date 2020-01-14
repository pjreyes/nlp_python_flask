import nltk
import numpy as np
import string,os,sys
from os import scandir, getcwd

from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
from nltk.corpus import stopwords

class CorpusIntents(object):

    def __init__(self, frase,filename):
        self.frase = frase
        self.filename = filename
        print(os.getcwd())
        # if os.getcwd() = os.getcwd()+'/corpus':
        #     os.chdir(os.getcwd()+'/corpus')
        self.f = open(self.filename,'r',errors = 'ignore')
        self.raw = self.f.read()
        self.raw = self.raw.lower()
        self.sent_tokens = nltk.sent_tokenize(self.raw)
        self.word_tokens = nltk.word_tokenize(self.raw)
        self.lemmer = nltk.stem.WordNetLemmatizer()
        self.remove_punct_dict = dict((ord(punct), None) for punct in string.punctuation)
        self.resultado = self.response(self.frase,self.filename)

    # def listFiles(ruta):
    #     return [arch.name for arch in scandir(ruta) if arch.is_file()]

    def LemTokens(self,tokens):
        return [self.lemmer.lemmatize(token) for token in tokens]

    # remove_punc_dict = dict((ord(punct), None) for punct in string.punctuation)

    def LemNormalize(self,text):
        return self.LemTokens(nltk.word_tokenize(text.lower().translate(self.remove_punct_dict)))

    def response(self,user_response,filename):
        self.sent_tokens.append(user_response)
        TfidVec = TfidfVectorizer(tokenizer=self.LemNormalize, stop_words=stopwords.words('spanish'))
        tfidf = TfidVec.fit_transform(self.sent_tokens)
        vals = cosine_similarity(tfidf[-1],tfidf)
        idx = vals.argsort()[0][-2]
        flat = vals.flatten()
        flat.sort()
        req_tfidf = flat[-2]
        filename = [x for x in filename.split("/")]
        print(str(filename)+" : "+str(req_tfidf))
        return {'intent':filename[len(filename)-1] , 'score': req_tfidf}
