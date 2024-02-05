import string
import argparse, math, os, re, string, zipfile
from typing import DefaultDict, Generator, Hashable, Iterable, List, Sequence, Tuple
from collections import defaultdict


f_1 = open("words.txt", "r")
f_2 = open("dict.txt", "r")

dict_1 = defaultdict(lambda: defaultdict(list))

lines_1 = f_1.readlines()
lines_2 = f_2.readlines()

for line in lines_1:
	first = line[0]
	second = ' '
	if len(line) >= 2:
		second = line[1]

	dict_1[first][second].append(line)

for line in lines_2:
	first = line[0]
	second = ' '
	if len(line) >= 2:
		second = line[1]
	if line not in dict_1[first][second]:
		dict_1[first][second].append(line)

f_1.close()
f_2.close()

f_3 = open("new.txt", "w")

for x in dict_1:
	for y in dict_1[x]:
		f_3.writelines(dict_1[x][y])
