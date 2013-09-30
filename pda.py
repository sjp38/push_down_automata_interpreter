#!/usr/bin/env python

__author__ = "SeongJae Park"
__email__ = "sj38.park@gmail.com"
__copyright__ = "Copyright (c) 2013, SeongJae Park"
__license__ = "GPLv3"

import sys

USAGE = """Usage: %s <pda file> [input file]""" % sys.argv[0]

class Stack:
    def __init__(self):
        self.data = []

    def push(self, value):
        self.data.append(value)

    def pop(self):
        ret = self.data[-1]
        del self.data[-1]
        return ret

    def head(self):
        if len(self.data) > 0:
            return self.data[-1]
        return None

    def empty(self):
        return len(self.data) == 0

    def __str__(self):
        return self.data.__str__()

class Transition:
    former_state = None
    next_state = None
    input_ = None
    pop = None
    push = None

    def __str__(self):
        return "%s: %s, %s > %s: %s" % (self.former_state, self.input_,
                self.pop, self.push, self.next_state)

# key: current state, value: transitions which former_state is key
TRANS = {}
CURRENT_STATE = 'q0'
STACK = Stack()

def _print_current_config():
    print "[current state]: ", CURRENT_STATE
    print "[current stack]: ", STACK
    print ""

def process_input(input_):
    global CURRENT_STATE
    if input_ != 'END' and CURRENT_STATE == 'q-1':
        return "\n[FAIL] End state before input end!"
    elif input_ == 'END' and CURRENT_STATE == 'q-1':
        return "\n[SUCCESS] Congratutation"

    transs = TRANS[CURRENT_STATE]
    found_trans = False
    for trans in transs:
        if (trans.former_state == CURRENT_STATE
                and trans.input_ == input_
                and (trans.pop == 'None'
                    or (trans.pop == 'Bottom' and STACK.empty())
                    or trans.pop == STACK.head())):
            _print_current_config()
            print "[do trans]: ", trans
            if trans.pop != 'None' and trans.pop != 'Bottom':
                STACK.pop()
            for push in trans.push:
                if push != 'None' and push != 'Bottom':
                    STACK.push(push)
            CURRENT_STATE = trans.next_state
            found_trans = True
            _print_current_config()
            break

    if not found_trans:
        return "\n[FAIL] Transition not found"
    return None

def _parse_pda_line(line):
    trans = Transition()
    line = line.replace(' ', '')
    line = line.replace('\n', '')
    splt = line.split(':')
    trans.former_state = splt[0]
    trans.next_state = splt[-1]

    splt = splt[1].split('>')
    trans.push = splt[1].split(',')

    splt = splt[0].split(',')
    trans.input_ = splt[0]
    trans.pop = splt[1]

    return trans

def parse_pda(file_):
    """
    parse pda configuration file.
    file may contain lines such as,
    q1: a,b>c: q2
    """
    for line in file_:
        if line.startswith('#') or line.startswith('\n'):
            continue
        trans = _parse_pda_line(line)
        if not trans.former_state in TRANS:
            TRANS[trans.former_state] = []
        TRANS[trans.former_state].append(trans) 


if __name__ == "__main__":
    """
    Parse pda file and process input from stdin.
    input can be terminated using predefined word, END
    """
    if len(sys.argv) < 2:
        print USAGE
        exit(1)
    with open(sys.argv[1], 'r') as f:
        parse_pda(f)

    while True:
        input_ = raw_input("pda>> ")
        result = process_input(input_)
        if result:
            break

    print result
