#!/usr/bin/env python3
"""
Unit tests for MyLang Programming Language
"""

from mylang import tokenize, Parser, Environment
import unittest
import sys
import os

# Add src to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'src'))


class TestMyLang(unittest.TestCase):
    """Test cases for MyLang language features"""

    def setUp(self):
        """Set up test environment"""
        self.env = Environment()

    def test_basic_arithmetic(self):
        """Test basic arithmetic operations"""
        code = "int result = 10 + 5; print(result);"
        tokens = tokenize(code)
        parser = Parser(tokens)
        ast = parser.parse()
        self.env.evaluate(ast)
        # If no exception is raised, test passes

    def test_variables(self):
        """Test variable declaration and assignment"""
        code = '''
        int x = 42;
        string msg = "Hello";
        bool flag = true;
        '''
        tokens = tokenize(code)
        parser = Parser(tokens)
        ast = parser.parse()
        self.env.evaluate(ast)

        # Check variables are stored correctly
        self.assertEqual(self.env.vars['x'][0], 42)
        self.assertEqual(self.env.vars['msg'][0], "Hello")
        self.assertEqual(self.env.vars['flag'][0], True)

    def test_function_definition(self):
        """Test function definition and calling"""
        code = '''
        func int add(int a, int b) {
            return a + b;
        }
        int result = add(5, 3);
        '''
        tokens = tokenize(code)
        parser = Parser(tokens)
        ast = parser.parse()
        self.env.evaluate(ast)

        # Check function was defined and called correctly
        self.assertEqual(self.env.vars['result'][0], 8)

    def test_control_flow(self):
        """Test if/else and while loops"""
        code = '''
        int x = 10;
        if (x > 5) {
            x = x * 2;
        } else {
            x = 0;
        }
        '''
        tokens = tokenize(code)
        parser = Parser(tokens)
        ast = parser.parse()
        self.env.evaluate(ast)

        self.assertEqual(self.env.vars['x'][0], 20)

    def test_type_conversions(self):
        """Test built-in type conversion functions"""
        code = '''
        string numStr = "42";
        int converted = toInt(numStr);
        '''
        tokens = tokenize(code)
        parser = Parser(tokens)
        ast = parser.parse()
        self.env.evaluate(ast)

        self.assertEqual(self.env.vars['converted'][0], 42)


if __name__ == '__main__':
    unittest.main()
