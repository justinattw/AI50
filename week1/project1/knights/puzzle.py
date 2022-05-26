"""
Knights puzzle

week1 project for 'cs50 introduction to artificial intelligence'
https://cs50.harvard.edu/ai/2020/projects/1/knights/
"""

from logic import *

AKnight = Symbol("A is a Knight")
AKnave = Symbol("A is a Knave")

BKnight = Symbol("B is a Knight")
BKnave = Symbol("B is a Knave")

CKnight = Symbol("C is a Knight")
CKnave = Symbol("C is a Knave")

# Puzzle 0
# A says "I am both a knight and a knave."
sentence0A = And(AKnight, AKnave)
knowledge0 = And(
    # AKnight XOR AKnave
    Biconditional(AKnight, Not(AKnave)),
    # A is a knight if and only if A is a knight and a knave
    Biconditional(AKnight, And(AKnight, AKnave))
)

# Puzzle 1
# A says "We are both knaves."
# B says nothing.
knowledge1 = And(
    # AKnight XOR AKnave
    Biconditional(AKnight, Not(AKnave)),
    # BKnight XOR BKnave
    Biconditional(BKnight, Not(BKnave)),
    # A is a knight if and only if A and B are knaves
    Biconditional(AKnight, And(AKnave, BKnave))
)


# Puzzle 2
# A says "We are the same kind."
# B says "We are of different kinds."
knowledge2 = And(
    # AKnight XOR AKnave
    Biconditional(AKnight, Not(AKnave)),
    # BKnight XOR BKnave
    Biconditional(BKnight, Not(BKnave)),
    # A is a knight if and only if A and B are of the same kind
    Biconditional(AKnight, Or(And(AKnight, BKnight), And(AKnave, BKnave))),
    # B is a knight if and only if A and B are different kinds
    Biconditional(BKnight, Or(And(AKnight, BKnave), And(AKnave, BKnight)))
)

# Puzzle 3
# A says either "I am a knight." or "I am a knave.", but you don't know which.
# B says "A said 'I am a knave'."
# B says "C is a knave."
# C says "A is a knight."
knowledge3 = And(
    # AKnight XOR AKnave
    Biconditional(AKnight, Not(AKnave)),
    # BKnight XOR BKnave
    Biconditional(BKnight, Not(BKnave)),
    # CKnight XOR CKnave
    Biconditional(CKnight, Not(CKnave)),
    # One of the following is true:
    #   A is a knight if and only if A is a knight
    #   A is a knight if and only if A is a knave
    Or(Biconditional(AKnight, AKnight), Biconditional(AKnight, AKnave)),
    # B is a knight if and only if (A is a knight if and only if A is a knave)
    Biconditional(BKnight, Biconditional(AKnight, AKnave)),
    # B is a knight if and only if C is a knave
    Biconditional(BKnight, CKnave),
    # C is a knight if and only if A is a knight
    Biconditional(CKnight, AKnight)
)


def main():
    symbols = [AKnight, AKnave, BKnight, BKnave, CKnight, CKnave]
    puzzles = [
        ("Puzzle 0", knowledge0),
        ("Puzzle 1", knowledge1),
        ("Puzzle 2", knowledge2),
        ("Puzzle 3", knowledge3)
    ]
    for puzzle, knowledge in puzzles:
        print(puzzle)
        if len(knowledge.conjuncts) == 0:
            print("    Not yet implemented.")
        else:
            for symbol in symbols:
                if model_check(knowledge, symbol):
                    print(f"    {symbol}")


if __name__ == "__main__":
    main()
