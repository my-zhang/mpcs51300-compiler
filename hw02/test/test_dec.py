import os 
import pytest 

from hw02.main import parser

TEST_DIR = os.path.dirname(__file__)

SAMPLE_DIR = os.path.join(TEST_DIR, 'samples')

def test_var_dec():
    assert [('VAR_DEC', 
             ('TYPE', 'int'), 
             [('INIT_ASSIGN', ('ID', 'sum'), ('ICONST', '1'))]
            )] == parser.parse("int sum = 1;")
