import jsonlines
import pickle
from pathlib import Path
import numpy as np
import pandas as pd
import spacy

def lemmatize(text):
    """Function to lemmatize text in one document."""
    doc = nlp(text)
    tokens = [token for token in doc if not token.is_punct]
    lemmas = [token.lemma_ if token.pos_ != 'PRON' else token.orth_ for token in tokens]
    for lemma in lemmas:
        if nlp.vocab[lemma].is_stop:
            lemmas.remove(lemma)
    return lemmas


def create_lemma_dict(data_file,out_file):
    """Function to convert a dictionary containing document text to a dictionary with lemmas for each document."""
    
    # Check if LEmma file has been created already
    outpath = Path(out_file)
    if outpath.is_file():
        with open(out_file,'rb') as oname:
            lemma_dict = pickle.load(oname)
        print("Found Lemma file")
        return lemma_dict
    else:
        print("Creating Lemma file")
        
        # Initialize global variables to be used by lemmatize() function
        global nlp, stopwords
        nlp = spacy.load('en_core_web_sm')
        stopwords = nlp.Defaults.stop_words
        
        # Check if data file exists
        datapath = Path(data_file)
        if datapath.is_file():
            with open(data_file,'rb') as fname:
                data_dict = pickle.load(fname)
        else:
            print("No data file")
            exit()
        
        # Lemmatize text in each document and add to Lemma dictionary
        lemma_dict = {}
        for i in data_dict.keys():
            lemma_dict.update({i : lemmatize(data_dict[i])})
        
        # Save a pickle file containing the Lemma dictionary
        with open(out_dict,'wb') as oname:
            pickle.dump(lemma_dict,oname)

        return lemma_dict

# Driver Code
data_file = 'data_dict.pkl'
out_file = 'lemma_dict.pkl' 

lemma_dict = create_lemma_dict(data_file,out_file) 
print("Lemma file created.")
