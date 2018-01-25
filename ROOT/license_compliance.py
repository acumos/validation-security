#!/usr/bin/env python 



"""
The following program is created based on Ninka, a language parser that is used in FOSSOLOGY. It provides a simple way to identify open source licenses in a source codefile. It is capable of identifying several dozen different licenses (and their variations).
"""


import os 
import sys
import re
from collections import Counter

# =============================================================================
#     This is a "spelling corrector" -- a work in progress activity
# =============================================================================

def words(text): return re.findall(r'\w+', text.lower())

WORDS = Counter(words(open('big.txt').read()))

def edits1(word):
    "All edits that are one edit away from `word`."
    letters    = 'abcdefghijklmnopqrstuvwxyz'
    splits     = [(word[:i], word[i:])    for i in range(len(word) + 1)]
    deletes    = [L + R[1:]               for L, R in splits if R]
    transposes = [L + R[1] + R[0] + R[2:] for L, R in splits if len(R)>1]
    replaces   = [L + c + R[1:]           for L, R in splits if R for c in letters]
    inserts    = [L + c + R               for L, R in splits for c in letters]
    return set(deletes + transposes + replaces + inserts)

def P(word, N=sum(WORDS.values())): 
    "Probability of `word`."
    return WORDS[word] / N

def edits2(word): 
    "All edits that are two edits away from `word`."
    return (e2 for e1 in edits1(word) for e2 in edits1(e1))

def correction(word): 
    "Most probable spelling correction for word."
    return max(candidates(word), key=P)

def candidates(word): 
    "Generate possible spelling corrections for word."
    return (known([word]) or known(edits1(word)) or known(edits2(word)) or [word])

def known(words): 
    "The subset of `words` that appear in the dictionary of WORDS."
    return set(w for w in words if w in WORDS)

#
# =============================================================================
#     This is the NLP parser - work in progress

# =============================================================================

def extract_features(word_list):
    return dict([(word, True) for word in word_list])
# Class to preprocess text
class Preprocessor(object):
    # Initialize various operators
    def __init__(self):
        # Create a regular expression tokenizer
        self.tokenizer = RegexpTokenizer(r'\w+')

        # get the list of stop words
        self.stop_words_english = stopwords.words('english')

        # Create a Snowball stemmer
        self.stemmer = SnowballStemmer('english')

    # Tokenizing, stop word removal, and stemming
    def process(self, input_text):
        # Tokenize the string
        tokens = self.tokenizer.tokenize(input_text.lower())

        # Remove the stop words
        tokens_stopwords = [x for x in tokens if not x in self.stop_words_english]

        # Perform stemming on the tokens
        #tokens_stemmed = [self.stemmer.stem(x) for x in tokens_stopwords]

        return tokens_stopwords





More_permission = ["PSFL","MIT","MIT (X11)", "New BSD", "ISC", "Apache" ]

Less_permissive = ["LGPL","GPL", "GPLv2", "GPLv3"]

Dict1 = {
"boostV1Ref" : "boostV1",
    "X11" : "X11mit",
    "X11Festival" : "X11mit",
    "X11mitNoSellNoDocDocBSDvar" : "X11mit",

    "X11mitwithoutSell" : 'X11mit',
    "X11mitBSDvar" : "X11mit",
    "X11mitwithoutSellCMUVariant" : "X11mit",
    "X11mitwithoutSellCMUVariant": "X11mit",
    "X11mitwithoutSellandNoDocumentationRequi" : "X11mit",
    "MITvar3" : "X11mit",
    "MITvar2" : "X11mit",
    "MIT" : "X11mit",
    "ZLIBref" : "ZLIB",
    "BSD3NoWarranty" : "BSD3",
    "BSD2EndorseInsteadOfBinary" : "BSD2",
    "BSD2var2" : "BSD2",
    "LesserGPLv2" : "LibraryGPLv2",
    "LesserGPLv2+"  : "LibraryGPLv2+",
    "orLGPLVer2.1" : "LesserGPLVer2.1",
    "postgresqlRef" : "postgresql"
    }

Dict2 = {
"MIT" : ['numpy','pandas']
"BSD" : ['scikit', 'gensim']
}

def License_compliance1():
    for i in list1:
        if i in Less_permissive:
            return ( 'Fail')
        else:
            return ("Pass")
