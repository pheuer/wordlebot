# -*- coding: utf-8 -*-
"""
@author: pheuer
"""

import os
import pandas as pd
import numpy as np
import time
import matplotlib.pyplot as plt

def _load_wordlist(path=os.path.join(os.getcwd(), 'wordlist', 'words.txt')):
    """
    Read in the word list from CSV
    
    Word list contains five-letter words and their frequencies
    """
    df = pd.read_csv(path, delimiter='\t')
    wordlist = [list(row) for row in df.values]
    return wordlist

class WordleBot:
    
    def __init__(self, firstword=None, answer=None, autoplay=False, verbose=None):
        self.wordlist = _load_wordlist()
        
        if firstword is None:
            self.word = 'earth'
        else:
            self.word = firstword
            
        # Used for autoplay
        self.answer = answer
        
        self.status = 'playing'
        self.quit = False
        self.turn = 0
        
        if autoplay:
            if verbose is None:
                self.verbose = False
            else:
                self.verbose = True
                
            while self.quit is False:
                self.auto_loop()
        else:
            self.verbose=True
            while self.quit is False:
                self.loop()
                
        self.summary()
        

    def printout(self, text):
        if self.verbose:
            print(text)

    
    def loop(self):
        """
        The main game loop
        """
        print("*************************************")
        print(f"Next word: {self.word}")    
        
        # Get user input
        result = self.get_input()
        self.process_input(result)
        
        # Choose a new word
        self.choose_word()
        
        # Increment the turn counter
        self.turn += 1
    
    
    
    def get_input(self):
        """
        Collect results from the current word from the user
        """
        
        no_input=True
        while no_input:
            user_input = input("g=green, y=yellow, x=black, q=quit "
                               "n=not in word list, w=won, l=lost\n"
                               "Input the pattern for the last word:")
            
            # Validate the input string as either a single letter command
            # or a 5-letter string of wordle results
            no_input=False
            if len(user_input) == 1:
                if user_input not in 'qnwl':
                    print("Invalid input")
                    no_input=True
            if len(user_input) == 5:
                if not set(user_input).issubset(set('gyx')):
                    print("Invalid input")
                    no_input=True
                    
                    
        return user_input
    
    
    def process_input(self, user_input):
        """
        Take input results (as a string of characters)
        """
            
        # Go through the input letter-by-letter
        for i in range(len(user_input)):
            letter = self.word[i]
            result = user_input[i]
            if result == 'g':
                # Eliminate words that don't have this letter at this location
                self.wordlist = [s for s in self.wordlist if s[0][i]==letter]
            elif result == 'y':
                # Eliminate words that don't contain this letter
                self.wordlist = [s for s in self.wordlist if letter in set(s[0])]
                # Eliminate words that have this letter at this location
                self.wordlist = [s for s in self.wordlist if s[0][i]!=letter]
            elif result == 'x':
                # Eliminate words that contain this letter
                self.wordlist = [s for s in self.wordlist if letter not in set(s[0])]
            elif result == 'n':
                # Remove this word from the word list and move on
                self.wordlist = [s for s in self.wordlist if s is not self.word]
                break
            elif result == 'q':
                # Quit the loop
                self.quit=True
            elif result == 'w':
                self.status='won'
                self.quit=True
            elif result == 'l':
                self.status = 'lost'
                self.quit=True
     
            
            
    def choose_word(self):
        """
        Choose the next word to play
        """
        wordlist = np.array(self.wordlist)
        # Arrays of the words and their frequencies
        words = wordlist[:,0]
        freq = wordlist[:,1].astype('int64')
        # An array of the number of unique letters in each word
        unique_letters = np.array([len(set(s)) for s in words])
        
        if self.turn <= 2:
            fitness = freq*unique_letters
        else:
            fitness = freq
             
        i = np.argmax(fitness)
        
        self.word = words[i]
        
        
    def get_input_auto(self):
        """
        Given an answer word, return the correct wordle string
        """
        wordlist = np.array(self.wordlist)
        words = set(wordlist[:,0])
 
        # Check if word is in word list
        if self.word not in words:
            return 'n'
        
        result = ''
        for i in range(len(self.word)):
            if self.word[i] == self.answer[i]:
                result += 'g'
            elif self.word[i] in self.answer:
                result += 'y'
            else:
                result += 'x'
                
        if result == 'ggggg':
            return 'w'
                
        return result
        
    
    
    def auto_loop(self):
        """
        The main game loop for automated play
        """
        self.printout("*************************************")
        self.printout(f"Answer: {self.answer}")
        self.printout(f"Word: {self.word}")
        # Get user input
        result = self.get_input_auto()
        self.printout(f"Result: {result}")
        self.process_input(result)
        
        # Choose a new word
        self.choose_word()
        
        # Increment the turn counter
        self.turn += 1
        
        if self.turn >= 7:
            self.status = 'lost'
            self.quit=True
            
            
    def summary(self):
        if self.status == 'won':
            self.printout(f"WORDLEBOT STRIKES AGAIN ({self.turn}/6)")
         
    @property
    def score(self):
        """
        Returns the score for a completed game
        
        lost -> zero points
        
        won ->  7 - turns
        
        so 
        
        (6/6) = 1 point
        (4/6) = 3 points
        (1/6) = 6 points

        """
        if self.status == 'lost':
            return 0
        
        elif self.status == 'won':
            return 7 - self.turn
        
        else:
            return np.nan
        
        

def test_wordlebot(num=300):
    """
    Test wordlebot on a random sample of 'num' words
    """
    # Load the wordlist
    wordlist = _load_wordlist()
    words = np.array(wordlist)[:,0]
    freq = np.array(wordlist)[:,1].astype('int64')
    
    # Draw a distribution of 'num' words
    p = freq/np.sum(freq)
    i = np.random.choice(np.arange(words.size), size=num, replace=False, p=p)
    words = words[i]
    
    # Create an array to store the scores
    results = np.zeros(num)
    # Run wordlebot auto mode for each answer word
    
    t0 = time.time()
    for i, answer in enumerate(words):
        if i % 50 == 0:
            print(f"Word {i}/{num}")
        # Run wordlebot
        g = WordleBot(answer=answer, autoplay=True)
        # Store the score
        results[i] = g.turn
    elapsed_time = (time.time()- t0)*1e3
    time_per_word = elapsed_time/num
        
    total_score = np.mean(results)
    
    print(f"Total score: {total_score:.2f}/6 ({time_per_word:.1f} ms/word)")
    
    fig, ax = plt.subplots(figsize=(6,6))
    ax.tick_params(axis='both', labelsize=12)
    ax.set_xticks([0,1,2,3,4,5,6])
    ax.set_xticklabels(['L', "1/6", "2/6", "3/6", "4/6", "5/6", "6/6"])
    
    ax.hist(results, bins=np.arange(8)-0.5)
    ax.set_xlabel("Score", fontsize=16)
    ax.set_ylabel("Test words", fontsize=16)
    ax.set_title(f"Mean score: {total_score:.2f}/6 on {num} words\n({time_per_word:.1f} ms/word)", fontsize=16)
    
    fig.savefig('results.png', dpi=300)
    
        

if __name__ == '__main__':
    #g = WordleBot(answer='earth', autoplay=True)

    test_wordlebot(num=500)   