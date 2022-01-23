# wordlebot
`Wordlebot` is a simple python algorithm for solving wordle puzzles, and can be run either manually with user input (to solve a wordle puzzle) or automatically using internally-generated puzzles (for benchmarking).
`Wordlebot` uses a lookup table of common five-letter English words and their frequencies in text to choose words.

# Manual Mode
To initialize `WordleBot` in manual mode: 

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
In automatic mode, `WordleBot` creates a Wordle puzzle from a given word and solves it automatically. This is used for benchmarking WordleBot automatically on thousands of words.

```python
g = WordleBot(answer='audio', verbose=True)
```
yields the output

```
*************************************
Answer: audio
Word: earth
Result: xyxxx
*************************************
Answer: audio
Word: black
Result: xxyxx
*************************************
Answer: audio
Word: audio
Result: w
WORDLEBOT STRIKES AGAIN (3/6)
```

# Benchmark WordleBot
`WordleBot` includes a benchmarking function that runs hundreds of puzzles (using words pulled from the word list) and records the number of turns required to solve them. 

```python
benchmark_wordlebot(num=500) 
```

Running this command results in a histogram showing the score distribution across the given words.

![results](https://user-images.githubusercontent.com/32618747/150688034-1e60b2b1-a4a3-42e0-a165-c4d1cfc6536c.png)

