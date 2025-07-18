#!/usr/bin/env python3
"""
Unit tests for MyLang Programming Language
"""

import unittest
import sys
import os

# Add src to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'src'))

from mylang import tokenize, Parser, Evaluator


class TestMyLang(unittest.TestCase):
    """Test cases for MyLang language features"""
    
    def setUp(self):
        """Set up test environment"""
        self.env = Evaluator()
    
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
        x_value, x_type = self.env.global_scope.get('x')
        msg_value, msg_type = self.env.global_scope.get('msg')
        flag_value, flag_type = self.env.global_scope.get('flag')
        
        self.assertEqual(x_value, 42)
        self.assertEqual(msg_value, "Hello")
        self.assertEqual(flag_value, True)
    
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
        result_value, result_type = self.env.global_scope.get('result')
        self.assertEqual(result_value, 8)
    
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
        
        x_value, x_type = self.env.global_scope.get('x')
        self.assertEqual(x_value, 20)
    
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
        
        converted_value, converted_type = self.env.global_scope.get('converted')
        self.assertEqual(converted_value, 42)


if __name__ == '__main__':
    unittest.main()
