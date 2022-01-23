# wordlebot
Wordlebot is a simple algorithm for solving wordle puzzles, and can be run either manually with user input (to solve a wordle puzzle) or automatically using internally-generated puzzles (for benchmarking).
Wordlebot uses a lookup table of common five-letter English words and their frequencies in text to choose words.

# Manual Mode
To initialize WordleBot in manual mode: 

```python
bot = WordleBot()
```

The prompt will then be displayed:

```
*************************************
Next word: earth

g=green, y=yellow, x=black, q=quit n=not in word list, w=won, l=lost
Input the pattern for the last word:
```

Where 'earth' is the first word chosen by the algorithm. Enter this word into Wordle, then provide the results back to the algorithm using the letters g, y and x to represent green, yellow, and black square respectively, eg.

```
gxxyx
```

The manual loop will continue until the puzzle is solved. 



# Automatic Mode



