import pytest
from crossword import *
from generate import *


def test_enforce_node_consistency():
    """
    GIVEN   a crossword and a crossword_creator domain
    WHEN    enforce_node_consistency() is called
    THEN    the unary constraints of each crossword variable and their associated domain should be satisfied
            (length of word)
    """
    crossword = Crossword("data/structure0.txt", "data/words0.txt")
    crossword_creator = CrosswordCreator(crossword)

    crossword_creator.enforce_node_consistency()

    for var in crossword.variables:
        for word in crossword_creator.domains[var]:
            assert len(word) == var.length

    print("hurrah")


def test_revise():
    crossword = Crossword("data/structure0.txt", "data/words0.txt")
    crossword_creator = CrosswordCreator(crossword)
    crossword_creator.enforce_node_consistency()
    for x in crossword.variables:
        for y in crossword.variables:
            if x == y:
                continue
            crossword_creator.revise(x, y)

    print("hurrah")

    # for x in crossword.variables:
    #     for y in crossword.variables:
    #         for x_word in crossword_creator.domains[x]:
    #             x_overlap, y_overlap = crossword.overlaps[x, y]
    #             assert crossword_creator.has_corresponding_value(x_word, x_overlap, y_overlap)

def test_ac3():
    crossword = Crossword("data/structure0.txt", "data/words0.txt")
    crossword_creator = CrosswordCreator(crossword)

    crossword_creator.enforce_node_consistency()
    crossword_creator.ac3()
    print("hurrah")

