import string
import argparse, math, os, re, string, zipfile
from typing import DefaultDict, Generator, Hashable, Iterable, List, Sequence, Tuple
from collections import defaultdict
import numpy as np
from sklearn import metrics
from blessed import Terminal
import tarfile

"""
    For optimal performance this program is to be run through your terminal while looking at an
    empty text file, called "final.txt", in ATOM. Once you have press enter in the command_line
    of the terminal, just start typing and you should be able to watch the characters write to your
    file. No program is ever perfect so there might be some random bugs that occur. I know of
    atleast one bug that, as of submitting this paper, I have spent 4 hours trying to find where the
    faulter is to no avail (sometimes after a somewhat random array of deletes and tabs without the
    spacebar being hit the program will not give another predicted word).
"""

class WordDictionary:
    """ Dictionary of english words """
    def __init__(self):
        self.word_dict = defaultdict(lambda: defaultdict(list))

    def build(self, file: str):
        """ Builds a bucket style dictionary to speed up look up speeds """
        #Opens and reads file
        file1 = open(file, "r")
        lines = file1.readlines()
        #Splits words into buckets
        for line in lines:
        	first = line.strip()[0]
        	second = ' '
        	if len(line.strip()) >= 2:
        		second = line.strip()[1]

        	self.word_dict[first][second].append(line.strip())

class Autofill:
    """Naive Bayes model for predicting text"""

    def __init__(self):
        """Create a new autofill model"""

        self.dict_1 = defaultdict(lambda: defaultdict(int))
        self.dict_total = defaultdict(int)

    #Not used with this data set. We chose to unlike punctuation so the program can do a premitive
    #predict for punctuation placement and will predict on words like "that,"
    def preprocess(self, example: List[str]) -> List[str]:
        """Normalize the string into a list of words.

        Args:
            example (str): Text input to split and normalize

        Returns:
            List[str]: Normalized words
        """

        example = example.translate(str.maketrans('', '', string.punctuation))
        example = example.lower()

        return example.split()

    def act_add_example(self, example: str, sentence: List[str]):
        """ Builds probability table off of both training data and actively as you type knew words

        Args:
            example (str): Word input to be added to tables
            sentence (List[str]): List of previous words written
        """

        #Double check to make sure we only have one word (had predictive problems)
        ex = example.split(" ")
        ex = ex[0]
        #Used while just starting your first sentence or for the first sentence of training data
        sent_len = len(sentence)
        #No words typed or added
        if sent_len == 0:
            self.dict_total[ex] += 1
        #After first word typed or added
        elif sent_len == 1:
            prev_1 = sentence[-1]

            self.dict_total[prev_1] += 1
            self.dict_1[prev_1][ex] += 1
        #After second word typed or added
        elif sent_len == 2:
            prev_1 = sentence[-1]
            prev_2 = sentence[-2] + " " + sentence[-1]

            self.dict_total[prev_1] += 1
            self.dict_1[prev_1][ex] += 1
            #self.dict_total[prev_2] += 2
            self.dict_1[prev_2][ex] += 4
        #After three words typed or added
        else:
            #Finds the preceding word combinations
            prev_1 = sentence[-1]
            prev_2 = sentence[-2] + " " + sentence[-1]
            prev_3 = sentence[-3] + " " + sentence[-2] + " " + sentence[-1]
            #Weighted because we want 3 words to have a stronger correlation
            #Part commented out are for a test
            self.dict_total[prev_1] += 1
            self.dict_1[prev_1][ex] += 1
            #self.dict_total[prev_2] += 2
            self.dict_1[prev_2][ex] += 4
            #self.dict_total[prev_3] += 3
            self.dict_1[prev_3][ex] += 9

    def remove_word(self, word: str, sentence: List[str]):
        """
        When we delete a word while typing it corrects the counts to represent what we actually
        want to type.

        Args:
            example (str): Word input to be removed from tables
            sentence (List[str]): List of previous words written
        """

        sent_len = len(sentence)
        #Used while just starting your first sentence or for the first sentence of training data
        #No words typed or added
        if sent_len == 0:
            #Lower prob associated with word
            self.dict_total[word] -= 1
            if self.dict_total[word] == 0:
                del self.dict_total[word]
        #After one word typed or added
        elif sent_len == 1:
            prev_1 = sentence[-1]
            #Lower prob associated with word and prev
            self.dict_total[prev_1] -= 1
            if self.dict_total[prev_1] == 0:
                del self.dict_total[prev_1]
            self.dict_1[prev_1][word] -= 1
            if self.dict_1[prev_1][word] == 0:
                del self.dict_1[prev_1][word]
        #After second word typed or added
        elif sent_len == 2:
            prev_1 = sentence[-1]
            prev_2 = sentence[-2] + " " + sentence[-1]

            #Lower prob associated with word and prev
            self.dict_total[prev_1] -= 1
            if self.dict_total[prev_1] == 0:
                del self.dict_total[prev_1]
            self.dict_1[prev_1][word] -= 1
            if self.dict_1[prev_1][word] == 0:
                del self.dict_1[prev_1][word]

            #self.dict_total[prev_2] -= 1
            #if self.dict_total[prev_2] == 0:
            #    del self.dict_total[prev_2]
            self.dict_1[prev_2][word] -= 4
            if self.dict_1[prev_2][word] == 0:
                del self.dict_1[prev_2][word]
        #After three or more word typed or added
        else:
            prev_1 = sentence[-1]
            prev_2 = sentence[-2] + " " + sentence[-1]
            prev_3 = sentence[-3] + " " + sentence[-2] + " " + sentence[-1]

            #Lower prob associated with word and prev
            self.dict_total[prev_1] -= 1
            if self.dict_total[prev_1] == 0:
                del self.dict_total[prev_1]
            self.dict_1[prev_1][word] -= 1
            if self.dict_1[prev_1][word] == 0:
                del self.dict_1[prev_1][word]

            #self.dict_total[prev_2] -= 1
            #if self.dict_total[prev_2] == 0:
            #    del self.dict_total[prev_2]
            self.dict_1[prev_2][word] -= 4
            if self.dict_1[prev_2][word] == 0:
                del self.dict_1[prev_2][word]

            #self.dict_total[prev_3] -= 1
            #if self.dict_total[prev_3] == 0:
            #    del self.dict_total[prev_3]
            self.dict_1[prev_3][word] -= 9
            if self.dict_1[prev_3][word] == 0:
                del self.dict_1[prev_3][word]

    def predict(self, sentence: List[str], word_list: List[str]) -> str:
        """ Predicts the most likely next word by comparing all words created through spell_check
            The if and else statements are to avoid iindexing errors into empty lists

            Args:
                sentence (List[str]): List of previous words written
                word_list (List[str]): List of possible spelling through our spell_check function

            Returns:
                str: Most probable next word
        """
        #Happens after spacebar or tab is hit, predicts the most likely next word before any more
        #keys are hit
        if len(word_list) == 0:
            #If nothing has been written yet, no suggestions
            if len(sentence) == 0:
                return ""
            #Only one word has been written
            elif len(sentence) == 1:
                if len(self.dict_1[sentence[-1]]) != 0:
                    #MAX returns the word as a string that has the highest count
                    return max(self.dict_1[sentence[-1]].items(), key=lambda a: a[1])[0]
                else:
                    return ""
            #Two words have been written
            elif len(sentence) == 2:
                if len(self.dict_1[sentence[-1]]) != 0:
                    best_1 = max(self.dict_1[sentence[-1]].items(), key=lambda a: a[1])
                else:
                    best_1 = [0, 0]
                if len(self.dict_1[sentence[-2] + " " + sentence[-1]]) != 0:
                    best_2 = max(self.dict_1[sentence[-2] + " " + sentence[-1]].items(), key=lambda a: a[1])
                else:
                    best_2 = [0, 0]
                #Picks most likely word campared to both two and one previous words
                return max([best_1, best_2] , key=lambda a: a[1])[0]
            #Three or more words have been written
            else:
                if len(self.dict_1[sentence[-1]]) != 0:
                    best_1 = max(self.dict_1[sentence[-1]].items(), key=lambda a: a[1])
                else:
                    best_1 = [0, 0]

                if len(self.dict_1[sentence[-2] + " " + sentence[-1]]) != 0:
                    best_2 = max(self.dict_1[sentence[-2] + " " + sentence[-1]].items(), key=lambda a: a[1])
                else:
                    best_2 = [0, 0]

                if len(self.dict_1[sentence[-3] + " " + sentence[-2] + " " + sentence[-1]]) != 0:
                    best_3 = max(self.dict_1[sentence[-3] + " " + sentence[-2] + " " + sentence[-1]].items(), key=lambda a: a[1])
                else:
                    best_3 = [0,0]
                #Picks most likely word campared to both three, two, and one previous words
                return max([best_1, best_2, best_3] , key=lambda a: a[1])[0]
        #Occurs when the writer might not be done typing (whether word is right or not)
        else:
            most_like = []
            #Works through list of possibly words
            for x in word_list:
                #Nothing has been written yet
                if len(sentence) == 0:
                    topval = defaultdict(int)
                    #iterate through dict_total and find words with prefix x
                    for y in self.dict_total:
                        #checks for word with same initial letters
                        if y.startswith(x):
                            topval[y] = self.dict_total[y]
                    if len(topval) != 0:
                        most_like.append(max(topval.items(), key = lambda a: a[1]))
                #Only one word has been written
                elif len(sentence) == 1:
                    prev = sentence[-1]

                    topval = defaultdict(int)
                    for y in self.dict_1[prev]:
                        if y.startswith(x):
                            topval[y] = self.dict_1[prev][y]
                    if len(topval) != 0:
                        most_like.append(max(topval.items(), key = lambda a: a[1]))
                #Two words have been written
                elif len(sentence) == 2:
                    prev_2 = sentence[-2] + " " + sentence[-1]
                    prev_1 = sentence[-1]

                    topval = defaultdict(int)
                    for y in self.dict_1[prev_2]:
                        if y.startswith(x):
                            topval[y] = self.dict_1[prev_2][y]

                    for y in self.dict_1[prev_1]:
                        if y.startswith(x):
                            topval[y] = self.dict_1[prev_1][y]
                    if len(topval) != 0:
                        most_like.append(max(topval.items(), key = lambda a: a[1]))
                #Three or more words have been written
                else:
                    prev_3 = sentence[-3] + " " + sentence[-2] + " " + sentence[-1]
                    prev_2 = sentence[-2] + " " + sentence[-1]
                    prev_1 = sentence[-1]

                    topval = defaultdict(int)
                    for y in self.dict_1[prev_3]:
                        if y.startswith(x):
                            topval[y] = self.dict_1[prev_3][y]

                    for y in self.dict_1[prev_2]:
                        if y.startswith(x):
                            topval[y] = self.dict_1[prev_2][y]

                    for y in self.dict_1[prev_1]:
                        if y.startswith(x):
                            topval[y] = self.dict_1[prev_1][y]
                    if len(topval) != 0:
                        most_like.append(max(topval.items(), key = lambda a: a[1]))
            #Returns the most likely word
            if len(most_like) == 0:
                return ""
            else:
                return max(most_like, key=lambda a: a[1])[0]

def spell_check(dictionary, actv_w: str) -> List[str]:
    """ Takes currently typed word, checks if in dictionary, if not return possible proper spelling

        Args:
            dictionary (WordDictionary): A data structure used as an english Dictionary
            actv_w (str): Input word being actively typed

        Returns:
            List[str]: List of english words transformed from actv_w
    """


    # Checks swap replacements
    def swap_char(wrong: str, dictionary) -> List[str]:
        fin_1 = []
        for i in range(len(wrong) - 1):
            temp = list(wrong)
            one = temp[i]
            temp[i] = temp[i+1]
            temp[i+1] = one
            temp = ''.join(temp)

            first = temp[0]
            second = ' '
            if len(temp) >= 2:
                second = temp[1]

            if temp in dictionary.word_dict[first][second]:
                fin_1.append(temp)

        return fin_1

	# Checks insert replacements
    def insert_char(wrong: str, dictionary) -> List[str]:
        fin_2 = []
        alph = "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ"
        for i in range(len(wrong) + 1):
            temp  = list(wrong)

            for j in range(len(alph)):
                temp  = list(wrong)
                temp.insert(i, alph[j])
                temp = ''.join(temp)

                first = temp[0]
                second = ' '
                if len(temp) >= 2:
                    second = temp[1]

                if temp in dictionary.word_dict[first][second]:
                    fin_2.append(temp)

        return fin_2

	#Checks delete replacements
    def delete_char(wrong: str, dictionary) -> List[str]:
        fin_3 = []
        for i in range(len(wrong)):
            temp = wrong
            temp = ''.join([wrong[j] for j in range(len(wrong)) if j != i])

            first = temp[0]
            second = ' '
            if len(temp) >= 2:
                second = temp[1]

            if temp in dictionary.word_dict[first][second]:
                fin_3.append(temp)

        return fin_3

	# Checks replace replacements
    def replace_char(wrong: str, dictionary) -> List[str]:
        fin_4 = []
        alph = "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ"
        for i in range(len(wrong)):
            temp = list(wrong)
            for j in range(len(alph)):
                temp[i] = alph[j]

                first = temp[0]
                second = ' '
                if len(temp) >= 2:
                    second = temp[1]

                if temp in dictionary.word_dict[first][second]:
                    fin_4.append(temp)

        return fin_4

	# Checks split replacements
    def split_char(wrong: str, dictionary) -> List[str]:
        fin_5 = []
        for i in range(len(wrong)):
            one = wrong[:i]
            two = wrong[i:]

            if len(one) != 0:
                first = one[0]
                second = ' '
                if len(one) >= 2:
                    second = one[1]

                if one in dictionary.word_dict[first][second]:
                    fin_5.append(one)

        return fin_5

    #Always add actively written word to the list even if it is not in dictionary
    suggestion = []
    suggestion.append(actv_w)

    first = actv_w[0]
    second = ' '
    if len(actv_w) >= 2:
        second = actv_w[1]
    #Checks if the actv_w is in dictionary
    if actv_w in dictionary.word_dict[first][second]:
        return suggestion
    #If not in dictionary, run through spell check methods creating list of english words
    else:
        #Run swap
        for x in swap_char(actv_w, dictionary):
            suggestion.append(x)
        #Run insert
        for x in insert_char(actv_w, dictionary):
            suggestion.append(x)
        #Run delete
        if len(actv_w) > 1:
            for x in delete_char(actv_w, dictionary):
                suggestion.append(x)
        #Run replace
        for x in replace_char(actv_w, dictionary):
            suggestion.append(x)
        #Run split
        for x in split_char(actv_w, dictionary):
            suggestion.append(x)

    return suggestion

if __name__ == "__main__":
    #Initialize model and dictionary
    model = Autofill()
    webster = WordDictionary()
    webster.build("new.txt")

    #Train model, used a famous book, language is a little dated
    sent = []
    with open('6593-0.txt','r') as file:
        # reading each line
        for line in file:
            # reading each word
            for word in line.split(" "):

                model.act_add_example(word, sent)
                sent.append(word)

                if len(sent) > 8:
                    sent = sent[4:]
    #Open writing file
    write_file = open("final.txt", "a+")

    #Initialize key strokes and language variables
    term = Terminal()
    word = ""
    suggest = ""
    sentence = []

    print("press 'esc' to quit.")
    #Start recording keystrokes in terminal
    with term.cbreak():
        val = u''
        #Checks if esc is pressed
        while format(str(val)) != "\x1b":
            #Warning after inactive for 5 minutes
            val = term.inkey(timeout=300)
            if not val:
                # timeout
                print("Warning, program will auto close in a minute")
                val = term.inkey(timeout=60)

                if not val:
                    val = "\x1b"
            #Check if delete or tab is pressed
            elif val.is_sequence and val != "\x1b":
                #Delete is hit
                if format(str(val)) == "\x7f":

                    write_file.close()
                    #Opens and reads lines
                    write_file = open("final.txt", "r+")
                    lines = write_file.readlines()
                    #Removes last character
                    lines[-1] = lines[-1][:-1]

                    write_file.close()
                    #Overwrites file
                    file1 = open("final.txt", "w")
                    file1.writelines(lines)
                    file1.flush()
                    file1.close()
                    #Reopens with header at the end
                    write_file = open("final.txt", "a+")

                    #delete after spacebar brings us back to previous word
                    if len(word) == 0:
                        if len(sentence) != 0:
                            #If word is "" then we have an error
                            word = sentence[-1]
                            sentence = sentence[:-1]
                            #Remove all extra spaces
                            while word == "":
                                write_file.close()
                                #Opens and reads lines
                                write_file = open("final.txt", "r+")
                                lines = write_file.readlines()
                                #Removes last character
                                lines[-1] = lines[-1][:-1]

                                write_file.close()
                                #Overwrites file
                                file1 = open("final.txt", "w")
                                file1.writelines(lines)
                                file1.flush()
                                file1.close()
                                #Reopens with header at the end
                                write_file = open("final.txt", "a+")

                                word = sentence[-1]
                                sentence = sentence[:-1]
                            #Removes word from prob tables and adjust all probs accordingly
                            model.remove_word(word, sentence)
                            #Creates list of words
                            spl_chk = spell_check(webster, word)
                            #Predicts next word
                            suggest = model.predict(sentence, spl_chk)
                            if suggest != 0 and suggest != "":
                                print(suggest)
                    #After one character we get empty word
                    elif len(word) == 1:
                        word = ""
                        suggest = model.predict(sentence, list(word))
                        if suggest != 0 and suggest != "":
                            print(suggest)
                    #removes last character of typed word
                    else:
                        word = word[:-1]
                        spl_chk = spell_check(webster, word)
                        suggest = model.predict(sentence, spl_chk)
                        if suggest != 0 and suggest != "":
                            print(suggest)

                #If tab is pressed we want to set word = suggestion, requires a space to confirm
                if format(str(val)) == "\t" and suggest != "":
                    word_len = len(word)
                    #This line makes word the top suggestion
                    word = suggest
                    #removes last word from file and then replaces with suggested word
                    write_file.close()

                    write_file = open("final.txt", "r+")
                    lines = write_file.readlines()

                    if word_len != 0:
                        lines[-1] = lines[-1][:-word_len]

                    write_file.close()

                    file1 = open("final.txt", "w")
                    file1.writelines(lines)
                    file1.flush()
                    file1.close()

                    write_file = open("final.txt", "a+")
                    if word != "":
                        write_file.write(word)
                    write_file.flush()


            elif val and val != "\x1b":

                #Write next character to file
                write_file.write(str(val))
                write_file.flush()

                #Spacebar hit
                if format(val) == ' ':
                    #add word to model or increase count
                    model.act_add_example(word, sentence)
                    sentence.append(word)
                    word = ""
                    suggest = model.predict(sentence, list(word))
                    if suggest != 0 and suggest != "":
                        print(suggest)
                #Any other character
                else:
                    word = word + val

                    """ Remember to change all predict to bottom """
                    spl_chk = spell_check(webster, word)
                    #print(spl_chk)
                    suggest = model.predict(sentence, spl_chk)

                    if suggest != 0 and suggest != "":
                        print(suggest)

        #print(model.dict_1)
        write_file.close()
        print('Thanks for writing')
