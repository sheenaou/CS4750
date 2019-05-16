#!/usr/bin/env python2

#########################################################
#  CS 4750 (Fall 2018), Assignment #1, Question #1     ##
#          Script File Name: tcomp1.py                 ##
#          Student Name: Sheena Ou                     ##
#          Login Name: so7122                          ##
#          MUN #: 20152395                             ##
#########################################################

"""
usage:
tcomp1.py master_file n file_to_compare1 file_to_compare2

Description:
Script takes a master text file, a value of n, and two or more comparison text files and prints
(1) the similarity of the master text file and each comparison text file
(2) the name of the comparison file that is most similar to the master text file
"""
import sys


def get_ngram(text_string, n):
    """Produces the ngrams in a string with a given n"""
    ngrams = []
    for i in range(0, len(text_string)):
        # iterate through the string and check if substring contains a whitespace
        if ' ' not in text_string[i:i + n] and i+n-1 < len(text_string):
            ngrams.append(text_string[i:i + n])
    return ngrams


def get_frequency(ngram):
    """Creates an frequency vector, whose indices match the associated ngram vector """
    freq = {}
    for gram in ngram:
        # calculate the number of occurrences of each element and divide by the length of the list
        freq[gram] = float(ngram.count(gram)) / len(ngram)
    return freq


def sim(x, y):
    """Calculates the similarity score between two text files"""
    # Get the frequency vector of both text files
    nmx = get_frequency(x)
    nmy = get_frequency(y)
    # Remove all duplicate entries
    ngrams = list(set(x) | set(y))
    total, diff = 0, 0
    # Calculate the sum of the absolute values of the difference in frequency of occurrence of each ngram
    for gram in ngrams:
        if gram in x:
            value1 = nmx.get(gram)
        else:
            value1 = 0.0
        if gram in y:
            value2 = nmy.get(gram)
        else:
            value2 = 0.0
        total = total + abs(value1-value2)
    diff = "%.3f" % float(1-total/2)
    return float(diff)


def main():
    """Compares similarity scores between the given text files and the master and states the highest"""
    master_file = open(sys.argv[1]).read().replace('\n', ' ').replace('\r', '').rstrip()
    num_files = int(sys.argv[2])
    sim_dictionary = {}
    for i in range(3, len(sys.argv)):
        compareFile = open(sys.argv[i]).read().replace('\n', ' ').replace('\r', '').rstrip()
        similar = sim(get_ngram(master_file, num_files), get_ngram(compareFile, num_files))
        print "Sim(", sys.argv[1], ", "+sys.argv[i], ") = ", similar
        sim_dictionary[sys.argv[i]] = similar
    max_value = max(sim_dictionary.values())  # maximum value
    max_key = [k for k, v in sim_dictionary.items() if v == max_value]
    print "File", max_key, "is the most similar to file", sys.argv[1]

main()
