#!/usr/bin/env python2

#########################################################
#  CS 4750 (Fall 2018), Assignment #2                  ##
#          Script File Name: reconstruct.py            ##
#          Student Name: Sheena Ou                     ##
#          Login Name: so7122                          ##
#          MUN #: 201523958                            ##
#########################################################

import sys


def readFST(filename):
    """Produces a FST based on the contents of a file given by filename."""
    lines = open(filename).read().split('\n')
    state_transition = {}   # [state_number : {input : output} ]
    for i in range(1, len(lines)):
        # check line for transition or state
        if lines[i] != "" and lines[i][0] != ' ':
            state = tuple(lines[i].upper().split(" "))
        else:
            # case: state does not exist in the fst
            if state not in state_transition:
                k = lines[i].lstrip().rfind(" ")
                key = lines[i].lstrip()[:k]
                value = lines[i].lstrip()[k + 1:]
                if lines[i].rstrip().lstrip() != "":
                    state_transition[state] = {key: list(value)}
                else:
                    state_transition[state] = ""
            # case: state already exist in the fst
            else:
                k = lines[i].lstrip().rfind(" ")
                key = lines[i].lstrip()[:k]
                value = lines[i].lstrip()[k + 1:]
                if key in state_transition[state]:
                    temp = list(state_transition[state][key])
                    temp.append(value)
                    state_transition[state][key] = temp
                else:
                    state_transition[state].update({key: list(value)})
    return state_transition


def composeFST(fst1, fst2):
    """Given two stored versions F1 and F2, create and return the FST that is F1 composed with F2."""
    new_fst = {}
    for state1 in fst1:
        for state2 in fst2:
            # determine state for new FST
            if state1[1] == "F" and state2[1] == "F":
                key = tuple([state1[0] + " " + state2[0], "F"])
            else:
                key = tuple([state1[0] + " " + state2[0], "N"])
            # EDGE CASE: either FST1 or FST2 has a null/empty transition
            if fst1[state1] == "" or fst2[state2] == "":
                if key not in new_fst:
                    new_fst[key] = ""
                else:
                    if value in new_fst[key]:
                        new_fst[key] = ""
                    else:
                        new_fst[key] = ""
            else:
                for transition_a in fst1[state1]:
                    list_a = transition_a.split(" ")
                    for transition_b in fst2[state2]:
                        list_b = transition_b.split(" ")
                        # CASE 1: ((q1,q2),x:epsilon,(q3,q2)) such that there are transitions (q1,x:epsilon,q3) in F1 and (q2,z:y,q4) in F2 where z is not epsilon
                        if list_a[1] == "-" and list_b[0] != "-":
                            value = list_a[0] + " " + list_a[1]
                            # for each possible final state in fst for that transition
                            for a in fst1[state1][transition_a]:
                                final_state = a + " " + state2[0]
                                if key not in new_fst:
                                    new_fst[key] = {value: [final_state]}
                                else:
                                    if value in new_fst[key]:
                                        new_fst[key][value].append(final_state)
                                    else:
                                        new_fst[key][value] = [final_state]

                        # CASE 2: ((q1,q2),epsilon:y,(q1,q4)) such that there are transitions (q1,x:z,q3) in F1 and (q2,epsilon:y,q4) in F2 where z is not epsilon.
                        if list_a[1] != "-" and list_b[0] == "-":
                            value = list_b[0] + " " + list_b[1]
                            for b in fst2[state2][transition_b]:
                                final_state = state1[0] + " " + b
                                if key not in new_fst:
                                    new_fst[key] = {value: [final_state]}
                                else:
                                    if value in new_fst[key]:
                                        new_fst[key][value].append(final_state)
                                    else:
                                        new_fst[key][value] = [final_state]

                        # CASE 3: ((q1,q2),x:y,(q3,q4)) such that there are transitions (q1,x:z,q3) in F1 and (q2,z:y,q4) in F2, where z can be any symbol (including epsilon))
                        if list_a[1] == list_b[0]:
                            value = list_a[0] + " " + list_b[1]
                            for a in fst1[state1][transition_a]:
                                for b in fst2[state2][transition_b]:
                                    final_state = a + " " + b
                                    if key not in new_fst:
                                        new_fst[key] = {value: [final_state]}
                                    else:
                                        if value in new_fst[key]:
                                            new_fst[key][value].append(final_state)
                                        else:
                                            new_fst[key][value] = [final_state]

    return new_fst


def get_state_type(state_number, fst):
    """Given a state, return whether the state is a final or non final"""
    for state in fst:
        if state[0] == state_number:
            return state[1]
    return


def reconstructUpper(lower, fst):
    """Print the set of upper strings associated with lower string l by FST F."""
    first_state = 0
    for state in fst:
        if list(set(state[0].split(" "))) == ['1']:
            first_state = state[0]
    constructUpper(lower, "", first_state, fst)


def constructUpper(lower, upper, state, fst):
    state_type = get_state_type(state, fst)
    lower = lower.replace("\n", "")
    if lower == "" and state_type == "F":
        print upper
        return
    elif lower == "" and str(state_type) != "F":
        return
    else:
        for transition in fst[tuple([state, state_type])]:
            temp = transition.split(" ")
            if temp[0] == "-":
                if temp[1] == "-":
                    constructUpper(lower, upper, fst[tuple([state, state_type])][transition][0], fst)
                else:
                    constructUpper(lower, upper + temp[1], fst[tuple([state, state_type])][transition][0], fst)
            elif temp[0] == lower[0]:
                if temp[1] == "-":
                    constructUpper(lower[1:], upper, fst[tuple([state, state_type])][transition][0], fst)
                else:
                    constructUpper(lower[1:], upper + temp[1], fst[tuple([state, state_type])][transition][0], fst)
        return


def reconstructLower(upper, fst):
    """Print the set of lower strings associated with upper string u by FST F."""
    first_state = 0
    for state in fst:
        if list(set(state[0].split(" "))) == ['1']:
            first_state = state[0]
    constructLower("", upper, first_state, fst)


def constructLower(lower, upper, state, fst):
    state_type = get_state_type(state, fst)
    upper = upper.replace("\n", "")
    if upper == "" and state_type == "F":
        print lower
        return
    elif upper == "" and state_type != "F":
        return
    else:
        for transition in fst[tuple([state, state_type])]:
            temp = transition.split(" ")
            if temp[1] == "-":
                if temp[0] == "-":
                    constructLower(lower, upper, fst[tuple([state, state_type])][transition][0], fst)
                else:
                    constructLower(lower + temp[0], upper, fst[tuple([state, state_type])][transition][0], fst)
            elif temp[1] == upper[0]:
                if temp[0] == "-":
                    constructLower(lower, upper[1:], fst[tuple([state, state_type])][transition][0], fst)
                else:
                    constructLower(lower + temp[0], upper[1:], fst[tuple([state, state_type])][transition][0], fst)
        return


def main():
    arguments = len(sys.argv)
    if arguments >= 4:  # script type form_file fst1 ... fstn
        form_file = list(open(sys.argv[2]))
        fst = readFST(sys.argv[3])
        number_transitions = 0
        if arguments >= 5:
            i = 4;
            while i != arguments:
                fst = composeFST(fst, readFST(sys.argv[i]))
                i = i + 1
        for state in fst:
            number_transitions = number_transitions + len(fst[state])
        if sys.argv[1].upper() == "SURFACE" or sys.argv[1].upper() == "LEXICAL":
            print "Composed FST has", len(fst), "states and ", number_transitions, "transitions"
            for line in form_file:
                new_line = line.replace('\n', '').lstrip().rstrip()
                if sys.argv[1].upper() == "SURFACE":
                    print "Lexical Form:", new_line
                    print "Surface Form(s):"
                    reconstructUpper(line, fst)
                    print "************************"
                elif sys.argv[1].upper() == "LEXICAL":
                    print "Surface Form:", new_line
                    print "Lexical Form(s):"
                    reconstructLower(line, fst)
                    print "************************"
        else:
            print "usage: reconstruct.py surface/lexical wlf/wsf F1 F2 ... Fn"
    else:
        print "usage: reconstruct.py surface/lexical wlf/wsf F1 F2 ... Fn"


main()

