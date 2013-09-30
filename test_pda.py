#!/usr/bin/env python

import unittest
import pda

class TestPda(unittest.TestCase):
    def setUp(self):
        print "test pda setup..."

    def tearDown(self):
        print "tear down..."

    def test_parse_pda_line(self):
        test_input = 'q0: None, a > b: q1\n'
        trans = pda._parse_pda_line(test_input)
        self.assertEqual(trans.former_state, 'q0')
        self.assertEqual(trans.input_, 'None')
        self.assertEqual(trans.pop, 'a')
        self.assertEqual(trans.push, ['b'])
        self.assertEqual(trans.next_state, 'q1')

        test_input = 'q0: a, Bottom > b,Bottom: q2'
        trans = pda._parse_pda_line(test_input)
        self.assertEqual(trans.push, ['b', 'Bottom'])

    def test_process_input(self):
        trans = pda.Transition()
        trans.former_state = 'q0'
        trans.next_state = 'q1'
        trans.input_ = 'a'
        trans.pop = 'Bottom'
        trans.push = 'b'

        pda.TRANS['q0'] = [trans]
        pda.process_input('a')

        self.assertEqual(pda.CURRENT_STATE, 'q1')
        self.assertEqual(pda.STACK.pop(), 'b')

    def test_stack(self):
        stack = pda.Stack()
        self.assertEqual(stack.empty(), True)
        self.assertEqual(stack.head(), None)
        stack.push(1)
        stack.push('ab')
        self.assertEqual(stack.pop(), 'ab')
        self.assertEqual(stack.head(), 1)
        self.assertEqual(stack.empty(), False)
        stack.pop()
        self.assertEqual(stack.empty(), True)

