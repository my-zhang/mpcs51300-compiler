import os 
import pytest 

from hw02.main import parser

TEST_DIR = os.path.dirname(__file__)

SAMPLE_DIR = os.path.join(TEST_DIR, 'samples')

def test_div():
    src = '''
            int main {
                int i = 4500;
                int j = -123;
                printd(i/j);
            }'''

    assert [('FUNC_DEF', ('TYPE', 'int'), 
                         ('ID', 'main'), 
                         ('COMP_STATS', 
                             [('VAR_DEC', ('TYPE', 'int'), [('INIT_ASSIGN', ('ID', 'i'), ('ICONST', '4500'))]), 
                              ('VAR_DEC', ('TYPE', 'int'), [('INIT_ASSIGN', ('ID', 'j'), ('NEG', ('ICONST', '123')))]), 
                              ('STAT', ('FUNC_CALL', ('ID', 'printd'), [('DIV', ('ID', 'i'), ('ID', 'j'))]))])) ] == \
            parser.parse(src)

