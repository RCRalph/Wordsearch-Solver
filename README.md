# Wordsearch Solver
Software that can solve wordsearches.

# System requirements
The software uses packages `sys` and `os`. Because of that, it is cross-platform and can be used on any operating system. To run the software you'll need Python 3.x.x and packages mentioned above. To install them, run `pip install sys` and `pip install os`. 

# Program usage
## Data input
To start using the software, run it in your operating system console. 

At first enter the amount of rows, that you want to check. Note that the software works only with rectangle wordsearches. Then enter the content of your wordsearch. Press `ENTER` key after every row you type in.

After entering the wordsearch content, please enter the amount of words to search for. Then type in all the words. Press `ENTER` key after every word you input.

## Program output
Example output is shown below:
```
The word "WORD" was found 2 times:

  1234
 ╔════╗
 ║W••D║1
 ║•OR•║2
 ║•OR•║3
 ║W••D║4
 ╚════╝
```
As you can see, the program output includes information like:
1. Amout of times the searched word was found.
1. Where on the wordsearch table the searched word is placed.

To exit, press the `ENTER` key.

# Additional content
In the folder `Wordsearch examples` you will find 5 text files, which contain example wordsearches that you can copy and use for testing.

# Created by RCRalph