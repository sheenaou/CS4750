#!/usr/bin/env python2


#########################################################
#  CS 4750 (Fall 2018), Assignment #1, Question #2     ##
#          Script File Name: tcomp2.py                 ##
#          Student Name: Sheena Ou                     ##
#          Login Name: so7122                          ##
#          MUN #: 20152395                             ##
#########################################################

"""
usage:
tcomp2.py master_file n file_to_compare1 file_to_compare2

Description:
Script takes a master text file, a value of n, and two or more comparison text files and prints
(1) the similarity of the master text file and each comparison text file
(2) the name of the comparison file that is most similar to the master text file
"""

import sys


def getWords(text_string):
    """Produces a list where each element is a word in the given text"""
    words = set(text_string.split(' '))
    words.discard("")
    return words


def getSimilar(string_x, string_y):
    """Produces the similarity score between two text files"""
    x_words = getWords(string_x)
    y_words = getWords(string_y)
    words = len(x_words) + len(y_words)
    unique = len(x_words.difference(y_words)) + len(y_words.difference(x_words))
    sim = "%.3f" % (1 - unique/float(words))
    return float(sim)


def main():
    """Compares similarity scores between the given text files and the master and states the highest"""
    master_file = open(sys.argv[1]).read().replace('\n', ' ').replace('\r', '').rstrip()
    sim_dict = {}
    for i in range(2, len(sys.argv)):
        compare_file = open(sys.argv[i]).read().replace('\n', ' ').replace('\r', '').rstrip()
        similar = getSimilar(master_file, compare_file)
        print "Sim(", sys.argv[1], ", "+sys.argv[i], ") = ", similar
        sim_dict[sys.argv[i]] = similar
    max_value = max(sim_dict.values())
    max_key = [k for k, v in sim_dict.items() if v == max_value]
    print "File", max_key, "is the most similar to file", sys.argv[1]


main()