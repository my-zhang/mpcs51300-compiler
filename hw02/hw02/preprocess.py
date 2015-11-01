import re
import sys

def remove_comment(source_code):
    """
    Remove C-sytle comments.
    """
    pattern = re.compile(r'//.*?$|/\*.*?\*/|\'(?:\\.|[^\\\'])*\'', re.DOTALL | re.MULTILINE)

    return re.sub(pattern, '', source_code)

def remove_blank(source_code):
    lines = source_code.split('\n')
    return '\n'.join(filter(lambda l: l, [l.strip() for l in lines]))

if __name__ == '__main__':
    s = sys.stdin.read()
    print remove_blank(remove_comment(s))
