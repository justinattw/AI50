import nltk
import os
import parser as p
import pytest

grammar = nltk.CFG.fromstring(p.NONTERMINALS + p.TERMINALS)
chart_parser = nltk.ChartParser(grammar)


def can_parse(s):
    # If filename specified, read sentence from file
    if os.path.isfile(s):
        with open(s) as f:
            sentence = f.read()
    else:
        sentence = s

    sentence = p.preprocess(sentence)

    # Attempt to parse sentence
    try:
        trees = list(chart_parser.parse(sentence))
    except ValueError as e:
        raise Exception(e)

    # return False if not trees else True

    if not trees:
        return False
    else:
        return True


@pytest.mark.parametrize(
    "test_input, expected",
    [
        ("sentences\\1.txt", True),
        ("sentences\\2.txt", True),
        ("sentences\\3.txt", True),
        ("sentences\\4.txt", True),
        ("sentences\\5.txt", True),
        ("sentences\\6.txt", True),
        ("sentences\\7.txt", True),
        ("sentences\\8.txt", True),
        ("sentences\\9.txt", True),
        ("sentences\\10.txt", True),
        ("Holmes sat in the armchair.", True),
        ("Holmes sat in the red armchair.", True),
        ("Holmes sat in the little red armchair.", True),
        ("Holmes sat in the the armchair.", False),
    ]
)
def test_invalid_sentence(test_input, expected):
    """
    GIVEN   a crossword and a crossword_creator domain
    WHEN    enforce_node_consistency() is called
    THEN    the unary constraints of each crossword variable and their associated domain should be satisfied
            (length of word)
    """
    assert can_parse(test_input) == expected
