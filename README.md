This repository has all the files I used in my Artificial Intelligence final project. 

My goal for the project was to create a program that acted similarly to Apple's imessage auto-correct and auto-suggest 
features. 

The end product: I was able to create a bayesian model for text prediction and crudely implements it.

Actually interfacing with my program is not the smoothest, however being an AI focussed project, the physical interaction 
was not the focal point. At any point I could go back and apply the meat of the code to a different UI.

Files:
6593_0.txt - This is a free publicly available book we trained the model on.
base_file.py - This is what we run on the command line to activate the program.
dict.txt - One of two dictionaries I combined together into new.txt
Final Project Diary.pdf - A record of what I did and the timeline
final.txt - This is the text file we are writing to, so after we run base_file.py we want this open to see what is happening
keyboard.py - File used to test key tracking capability and auto closing function
new.txt - This is our combined dictionary with over 78,000 words, created by test.py
test.py - Joins two dictionaries
words.txt - One of two dictionaries I combined together into new.txt

How to run program: (All of this was done in MAC terminal)
For optimal performance type and enter "python3 base_file.py" in your terminal. Make sure you have installed the numpy, sklearn, and blessed
modules using "pip3 instal ____". Then open the empty text file, called "final.txt", in ATOM. Once you have press enter in the command_line 
of the terminal, just start typing and you should be able to watch the characters write to your file. The autocompleted words and next suggested
words will show up in the terminal. You can autofill the words by pressing the "TAB" key. If you do not interact with the program for 5 minutes
a warning will pop up and if, after another minute, no action is take, the program will automatically terminate. You can also quit the program 
by pressing the "ESC" key.

Bugs:
No program is ever perfect so there might be some random bugs that occur. I know of atleast one bug that I have spent 4 hours trying to find 
where the faulter is to no avail. The bug is, sometimes after a somewhat random sequence of deletes and tabs without the spacebar being hit 
the program will not give another predicted word.
