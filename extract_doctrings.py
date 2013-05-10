# Extract picosat documentation from .h

import re
import os

def find_comments(corpus):
    declaration = re.compile(r"""(int|void)\s(?P<name>\w+)""", re.MULTILINE)
    pos = 0
    begin = 0
    end = 0
    while begin >= 0 and end >= 0:
        begin = corpus.find("/*", pos)
        end = corpus.find("*/", begin)
        nextdecl = declaration.search(corpus, end, end+160)
        name = ''
        if nextdecl:
            name = nextdecl.groupdict()['name']
        yield (name, clean_comment(corpus[begin:end]))
        pos = end + 2

def clean_comment(comment):
    cleaned = []
    for line in comment.splitlines():
        cleaned.append(re.sub(r"^(\s*(\/?\*)\s?)", "", line))
    return '\n'.join(cleaned)

def comment_map():
    """Return a mapping {likely_name : comment} for comments in picosat.h"""
    corpus = open(os.path.join('picosat-956', 'picosat.h'), 'r').read()
    return dict(find_comments(corpus))
