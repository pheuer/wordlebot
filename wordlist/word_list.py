# -*- coding: utf-8 -*-
"""
Create a list of valid wordle words
"""


import os
import pandas as pd


def create_words():
    """
    The initial dataset is from the National Language Corpus Data:
    https://norvig.com/ngrams/

    """
    df = pd.read_csv('count_1w.txt', delimiter='\t')
    
    words = [list(row) for row in df.values]
    
    # Eliminate all but 5 letter words
    words = [s for s in words if len(str(s[0]))==5]
    
    # Truncate the word list based on frequency
    words = words[0:7000]
    
    #print(len(words))
    print(words[-50:-1])
    
    
    
    if os.path.isfile('words.txt'):
        os.remove('words.txt')
    with open('words.txt', 'w') as f:
        for s in words:
            f.write(f"{s[0]}\t{s[1]}\n")
            
            
if __name__ == "__main__":
    
    create_words()