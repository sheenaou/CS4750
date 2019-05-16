#!/usr/bin/env python2

#########################################################
#  CS 4750 (Fall 2018), Assignment #3                  ##
#          Script File Name: CKYdet.py                 ##
#          Student Name: Sheena Ou                     ##
#          Login Name: so7122                          ##
#          MUN #: 201523958                            ##
#########################################################

import sys


def main():
    # if len(sys.argv) < 3:
    #     print "usage: python CKYdet.py grammar_file utterance_file"
    # else:
        grammar = get_grammar(open(sys.argv[1]))
        utterance = get_utterance(open(sys.argv[2]))
        count = 1
        for case in utterance:
            matrix = get_blank_matrix(case)
            fill_base_case(matrix, case, grammar)
            fill_other_cases(matrix, case, grammar)
            if check_valid(matrix):
                parses = get_parse(matrix)
                parse_case = 1
                print "CASE", count, ": this is a valid parse"
                for parse in parses:
                    print "PARSE", parse_case,"==>", parse
                    parse_case = parse_case + 1
            else:
                print "CASE", count, ": no valid parse"
            print "----------------------------------"
            count = count + 1


def get_utterance(file):
    """returns a list of utterances in a file"""
    utterance = []
    for line in file:
        temp = line.strip().split(" ")
        utterance.append(temp)
    return utterance


def get_grammar(file):
    """converts a grammar file into dictionary form"""
    grammar = {}
    for line in file:
        temp = line.strip().split("->")
        key = temp[0].strip()
        value = temp[1].replace('\"', '') .strip().split(" ")
        if key not in grammar:
            grammar[key] = [value]
        else:
            grammar[key].append(value)
    return grammar


def print_grammar(grammar):
    """helper function to print grammar dictionary"""
    for key in grammar:
        print key, "-->", grammar[key]


def get_blank_matrix(utterance):
    """creates a blank matrix based on the #words in the utterance"""
    length = len(utterance)
    matrix = []
    for i in range(0,length):
        matrix.append([["-"]])
        for j in range(0, length-i-1):
            matrix[i].append(["-"])
    return matrix


def print_matrix(matrix):
    """helper function to print the matrix"""
    for line in range(0, len(matrix)):
        print line, ":", matrix[line]


def fill_base_case(matrix, utterance, grammar):
    """fill the matrix with the base case of each word in the utterance"""
    index = 0
    #CASE 1 - add the base case of each word
    for word in utterance:
        for key in grammar:
            if [word] in grammar[key]:
                value = "[" + key+" \""+word+"\"" +"]"
                if matrix[index][0] != ["-"]:
                    matrix[index][0].append([key,value])
                else:
                    matrix[index][0] = [[key,value]]
        index = index + 1
    #CASE 2 - for each base case added, check if the case has a transition to another non terminal
    for index in range(0, len(matrix)):
        for number in range(0, len(matrix[index][0])):
            for key in grammar:
                list = matrix[index][0][number]
                if [list[0]] in grammar[key]:
                    value = "[" + key+" " +list[1] + "]"
                    if matrix[index][0] != ["-"]:
                        matrix[index][0].append([key, value])


def fill_other_cases(matrix, utterance, grammar):
    """fill in the rest of the matrix"""
    length = len(utterance)
    for y in range(1, length):
        for x in range(0, length-y):
            #get initial coordinates
            x0 = x
            y0 = 0
            x1 = x + 1
            y1 = y - 1
            for index in range(0,y):
                value_1 = matrix[x0][y0]
                value_2 = matrix[x1][y1]

                #CASE A - check the matrix to see if  other parses
                for case_1 in value_1:
                    for case_2 in value_2:
                        possible_value = [case_1[0], case_2[0]]
                        for key in grammar:
                            if possible_value in grammar[key]:
                                string = "[" + key + " " + case_1[1] + case_2[1] + "]"
                                if matrix[x][y] != ["-"]:
                                    matrix[x][y].append([key, string])
                                else:
                                    matrix[x][y] = [[key,string]]
                #CASE B - if any parses are added, check if the parse leads to another non terminal
                for index in range(0, len(matrix[x][y])): #go over the elements that exist
                    for element in matrix[x][y]:
                        if element != '-':
                            possible_case = [element[0]]
                            possible_string = element[1]
                            for key in grammar:
                                if possible_case in grammar[key]:
                                    string = "[" + key + " " + possible_string + "]"
                                    if matrix[x][y] != ["-"]:
                                        if [key,string] not in matrix[x][y]:
                                            matrix[x][y].append([key, string])
                                    else:
                                        matrix[x][y] = [[key, string]]
                y0 = y0 + 1
                x1 = x1 + 1
                y1 = y1 - 1


def check_valid(matrix):
    """Check if there is a valid parse for the utterance """
    length = len(matrix)-1
    test = matrix[0][length]
    for case in matrix[0][length]:
        if case[0] == 'S':
            return True
    return False


def get_parse(matrix):
    """returns a list of all valid parses"""
    parses = []
    length = len(matrix)-1
    for entry in matrix[0][length]:
        if entry[0] == "S":
            parses.append(entry[1])
    return parses


main()