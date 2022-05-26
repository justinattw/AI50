"""
Crossword project

week3 project for 'cs50 introduction to artificial intelligence'
https://cs50.harvard.edu/ai/2020/projects/3/crossword/
"""

import math
import sys

from crossword import *


class CrosswordCreator():

    def __init__(self, crossword):
        """
        Create new CSP crossword generate.
        """
        self.crossword = crossword
        self.domains = {
            var: self.crossword.words.copy()
            for var in self.crossword.variables
        }

    def letter_grid(self, assignment):
        """
        Return 2D array representing a given assignment.
        """
        letters = [
            [None for _ in range(self.crossword.width)]
            for _ in range(self.crossword.height)
        ]
        for variable, word in assignment.items():
            direction = variable.direction
            for k in range(len(word)):
                i = variable.i + (k if direction == Variable.DOWN else 0)
                j = variable.j + (k if direction == Variable.ACROSS else 0)
                letters[i][j] = word[k]
        return letters

    def print(self, assignment):
        """
        Print crossword assignment to the terminal.
        """
        letters = self.letter_grid(assignment)
        for i in range(self.crossword.height):
            for j in range(self.crossword.width):
                if self.crossword.structure[i][j]:
                    print(letters[i][j] or " ", end="")
                else:
                    print("█", end="")
            print()

    def save(self, assignment, filename):
        """
        Save crossword assignment to an image file.
        """
        from PIL import Image, ImageDraw, ImageFont
        cell_size = 100
        cell_border = 2
        interior_size = cell_size - 2 * cell_border
        letters = self.letter_grid(assignment)

        # Create a blank canvas
        img = Image.new(
            "RGBA",
            (self.crossword.width * cell_size,
             self.crossword.height * cell_size),
            "black"
        )
        font = ImageFont.truetype("assets/fonts/OpenSans-Regular.ttf", 80)
        draw = ImageDraw.Draw(img)

        for i in range(self.crossword.height):
            for j in range(self.crossword.width):

                rect = [
                    (j * cell_size + cell_border,
                     i * cell_size + cell_border),
                    ((j + 1) * cell_size - cell_border,
                     (i + 1) * cell_size - cell_border)
                ]
                if self.crossword.structure[i][j]:
                    draw.rectangle(rect, fill="white")
                    if letters[i][j]:
                        w, h = draw.textsize(letters[i][j], font=font)
                        draw.text(
                            (rect[0][0] + ((interior_size - w) / 2),
                             rect[0][1] + ((interior_size - h) / 2) - 10),
                            letters[i][j], fill="black", font=font
                        )

        img.save(filename)

    def solve(self):
        """
        Enforce node and arc consistency, and then solve the CSP.
        """
        self.enforce_node_consistency()
        self.ac3()
        return self.backtrack(dict())

    def enforce_node_consistency(self):
        """
        Update `self.domains` such that each variable is node-consistent.
        (Remove any values that are inconsistent with a variable's unary
         constraints; in this case, the length of the word.)
        """
        # TODO

        for var in self.domains.keys():
            self.domains[var] = [word for word in self.domains[var] if len(word) == var.length]

    def revise(self, x, y):
        """
        Make variable `x` arc consistent with variable `y`.
        To do so, remove values from `self.domains[x]` for which there is no
        possible corresponding value for `y` in `self.domains[y]`.

        Return True if a revision was made to the domain of `x`; return
        False if no revision was made.
        """
        # TODO
        revised = False

        overlap = self.crossword.overlaps[x, y]
        if not overlap:
            return False

        i, j = overlap
        for x_word in self.domains[x]:
            x_word_removed = False
            for y_word in self.domains[y]:
                if x_word[i] != y_word[j]:  # Constraint
                    self.domains[x].remove(x_word)
                    revised = True
                    x_word_removed = True
                if x_word_removed:
                    break

        return revised

    def ac3(self, arcs=None):
        """
        Update `self.domains` such that each variable is arc consistent.
        If `arcs` is None, begin with initial list of all arcs in the problem.
        Otherwise, use `arcs` as the initial list of arcs to make consistent.

        Return True if arc consistency is enforced and no domains are empty;
        return False if one or more domains end up empty.
        """
        # TODO

        if not arcs:
            queue = []
            for var in self.domains.keys():
                neighbors = self.crossword.neighbors(var)
                for neighbor in neighbors:
                    queue.append((var, neighbor))
        else:
            queue = arcs

        while queue:
            (x, y) = queue.pop()  # Dequeue: remove x, y from arcs

            if self.revise(x, y):
                # If there is nothing left in a variable's domain, there is no way to solve the problem
                if len(self.domains[x]) == 0:
                    return False
                for neighbor in self.crossword.neighbors(x):
                    if neighbor != y:
                        queue.append((neighbor, x))  # Enqueue neighbor, X

        return True

    def assignment_complete(self, assignment):
        """
        Return True if `assignment` is complete (i.e., assigns a value to each
        crossword variable); return False otherwise.
        """
        # TODO

        for word in assignment:  # TODO: what does assignment look like?
            if not word:
                return False

        return True

    def consistent(self, assignment):
        """
        Return True if `assignment` is consistent (i.e., words fit in crossword
        puzzle without conflicting characters); return False otherwise.
        """
        # TODO

        fails_unary_constraints = False
        for var in assignment.keys():
            if var.length != assignment[var]:
                fails_unary_constraints = True

        fails_binary_constraints = False
        for x_var in assignment.keys():
            for y_var in assignment.keys():
                if x_var != y_var:
                    i, j = self.crossword.overlaps(x_var, y_var)
                    if assignment[x_var][i] != assignment[y_var][j]:
                        fails_binary_constraints = True

        return fails_unary_constraints or fails_binary_constraints

    def order_domain_values(self, var, assignment):
        """
        Return a list of values in the domain of `var`, in order by
        the number of values they rule out for neighboring variables.
        The first value in the list, for example, should be the one
        that rules out the fewest values among the neighbors of `var`.
        """
        # TODO


        raise NotImplementedError

    def select_unassigned_variable(self, assignment):
        """
        Return an unassigned variable not already part of `assignment`.
        Choose the variable with the minimum number of remaining values
        in its domain. If there is a tie, choose the variable with the highest
        degree. If there is a tie, any of the tied variables are acceptable
        return values.
        """
        # TODO

        unassigned_vars = self.domains.keys() - assignment.keys()
        smallest_domain_size = math.inf
        vars_with_smallest_domain = []
        for var in unassigned_vars:
            domain_size = len(self.domains[var])
            if domain_size < smallest_domain_size:
                smallest_domain_size = domain_size
                vars_with_smallest_domain = [var]
            elif domain_size == smallest_domain_size:
                vars_with_smallest_domain.append(var)

        if len(vars_with_smallest_domain) == 1:
            return vars_with_smallest_domain[0]
        elif len(vars_with_smallest_domain) > 1:
            most_neighbors_num = 0
            var_with_most_neighbors = None
            for var in vars_with_smallest_domain:
                neighbors_num = len(self.crossword.neighbors(var))
                if neighbors_num > most_neighbors_num:
                    var_with_most_neighbors = var
                    most_neighbors_num = neighbors_num

            if var_with_most_neighbors:
                return var_with_most_neighbors
            else:
                raise Exception("No variables with most neighbors were found.")
        else:
            raise Exception("There are no variables with the smallest domain.")

    def backtrack(self, assignment):
        """
        Using Backtracking Search, take as input a partial assignment for the
        crossword and return a complete assignment if possible to do so.

        `assignment` is a mapping from variables (keys) to words (values).

        If no assignment is possible, return None.
        """
        # TODO

        if self.assignment_complete(assignment):
            return assignment

        else:
            pass
            self.backtrack(assignment)

        return 0
        raise NotImplementedError


def main():
    # Check usage
    if len(sys.argv) not in [3, 4]:
        sys.exit("Usage: python generate.py structure words [output]")

    # Parse command-line arguments
    structure = sys.argv[1]
    words = sys.argv[2]
    output = sys.argv[3] if len(sys.argv) == 4 else None

    # Generate crossword
    crossword = Crossword(structure, words)
    creator = CrosswordCreator(crossword)
    assignment = creator.solve()

    # Print result
    if assignment is None:
        print("No solution.")
    else:
        creator.print(assignment)
        if output:
            creator.save(assignment, output)


if __name__ == "__main__":
    main()
