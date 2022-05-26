"""
Heredity project

week2 project for 'cs50 introduction to artificial intelligence'
https://cs50.harvard.edu/ai/2020/projects/2/heredity/
"""

import csv
import itertools
import sys

PROBS = {

    # Unconditional probabilities for having gene
    "gene": {
        2: 0.01,
        1: 0.03,
        0: 0.96
    },

    "trait": {

        # Probability of trait given two copies of gene
        2: {
            True: 0.65,
            False: 0.35
        },

        # Probability of trait given one copy of gene
        1: {
            True: 0.56,
            False: 0.44
        },

        # Probability of trait given no gene
        0: {
            True: 0.01,
            False: 0.99
        }
    },

    # Mutation probability
    "mutation": 0.01
}


def main():
    # Check for proper usage
    if len(sys.argv) != 2:
        sys.exit("Usage: python heredity.py data.csv")
    people = load_data(sys.argv[1])

    # Keep track of gene and trait probabilities for each person
    probabilities = {
        person: {
            "gene": {
                2: 0,
                1: 0,
                0: 0
            },
            "trait": {
                True: 0,
                False: 0
            }
        }
        for person in people
    }

    # Loop over all sets of people who might have the trait
    names = set(people)
    for have_trait in powerset(names):

        # Check if current set of people violates known information
        fails_evidence = any(
            (people[person]["trait"] is not None and
             people[person]["trait"] != (person in have_trait))
            for person in names
        )
        if fails_evidence:
            continue

        # Loop over all sets of people who might have the gene
        for one_gene in powerset(names):
            for two_genes in powerset(names - one_gene):
                p = joint_probability(people, one_gene, two_genes, have_trait)
                update(probabilities, one_gene, two_genes, have_trait, p)

    # Ensure probabilities sum to 1
    normalize(probabilities)

    # Print results
    for person in people:
        print(f"{person}:")
        for field in probabilities[person]:
            print(f"  {field.capitalize()}:")
            for value in probabilities[person][field]:
                p = probabilities[person][field][value]
                print(f"    {value}: {p:.4f}")


def load_data(filename):
    """
    Load gene and trait data from a file into a dictionary.
    File assumed to be a CSV containing fields name, mother, father, trait.
    mother, father must both be blank, or both be valid names in the CSV.
    trait should be 0 or 1 if trait is known, blank otherwise.
    """
    data = dict()
    with open(filename) as f:
        reader = csv.DictReader(f)
        for row in reader:
            name = row["name"]
            data[name] = {
                "name": name,
                "mother": row["mother"] or None,
                "father": row["father"] or None,
                "trait": (True if row["trait"] == "1" else
                          False if row["trait"] == "0" else None)
            }
    return data


def powerset(s):
    """
    Return a list of all possible subsets of set s.
    """
    s = list(s)
    return [
        set(s) for s in itertools.chain.from_iterable(
            itertools.combinations(s, r) for r in range(len(s) + 1)
        )
    ]


def get_num_genes(person, one_gene, two_genes):
    """
    Get the specified number of genes for `person`
    """
    if person in one_gene:
        return 1
    elif person in two_genes:
        return 2
    else:
        return 0


def passed_on_gene_probability(num_genes):
    """
    Given the number of genes `num_genes` of a person, find the probability that they pass the gene down to their child.
    """
    prob_mutation = PROBS["mutation"]  # 0.01
    prob_not_mutation = 1 - prob_mutation  # 0.99

    if num_genes == 2:
        return prob_not_mutation
    elif num_genes == 1:
        return (0.5 * prob_mutation) + (0.5 * prob_not_mutation)
    else:
        return prob_mutation


def inheritance_probability(child_num_genes, parent_a_num_genes, parent_b_num_genes):
    """
    Find P(child_num_genes | parent_a_num_genes, parent_b_num_genes)
    """
    parent_a_passed_on_gene = passed_on_gene_probability(parent_a_num_genes)
    parent_b_passed_on_gene = passed_on_gene_probability(parent_b_num_genes)
    parent_a_did_not_pass_on_gene = 1 - parent_a_passed_on_gene
    parent_b_did_not_pass_on_gene = 1 - parent_b_passed_on_gene

    # If child has 2 genes, find probability that both parents passed on genes
    if child_num_genes == 2:
        return parent_a_passed_on_gene * parent_b_passed_on_gene

    # If child has 1 gene, find probability that one parent passed on gene, while the other didn't
    elif child_num_genes == 1:
        return ((parent_a_passed_on_gene * parent_b_did_not_pass_on_gene) +
                (parent_a_did_not_pass_on_gene * parent_b_passed_on_gene))

    # If child has 0 genes, find probability that neither parents passed on gene
    else:
        return parent_a_did_not_pass_on_gene * parent_b_did_not_pass_on_gene


def joint_probability(people, one_gene, two_genes, have_trait):
    """
    Compute and return a joint probability.

    The probability returned should be the probability that
        * everyone in set `one_gene` has one copy of the gene, and
        * everyone in set `two_genes` has two copies of the gene, and
        * everyone not in `one_gene` or `two_gene` does not have the gene, and
        * everyone in set `have_trait` has the trait, and
        * everyone not in set` have_trait` does not have the trait.
    """
    probability = 1
    for person in people:
        num_genes = get_num_genes(person, one_gene, two_genes)  # 0, 1, or 2
        has_trait = person in have_trait                        # true or false

        if not people[person]["mother"]:
            # If person has not parents, then gene prob distribution follows unconditional probability distribution
            probability *= PROBS["gene"][num_genes]
        else:
            mother_num_genes = get_num_genes(people[person]["mother"], one_gene, two_genes)
            father_num_genes = get_num_genes(people[person]["father"], one_gene, two_genes)
            # If person has parents, then inheritance probability follows the inheritance conditional probabilities.
            probability *= inheritance_probability(num_genes, mother_num_genes, father_num_genes)

        # Multiply by (conditional) probability of trait given the number of genes
        probability *= PROBS["trait"][num_genes][has_trait]

    return probability


def update(probabilities, one_gene, two_genes, have_trait, p):
    """
    Add to `probabilities` a new joint probability `p`.
    Each person should have their "gene" and "trait" distributions updated.
    Which value for each distribution is updated depends on whether
    the person is in `have_gene` and `have_trait`, respectively.
    """
    for person in probabilities.keys():
        num_genes = get_num_genes(person, one_gene, two_genes)  # 0, 1, or 2
        probabilities[person]["gene"][num_genes] += p

        has_trait = person in have_trait  # True, False
        probabilities[person]["trait"][has_trait] += p

    return probabilities


def normalize(probabilities):
    """
    Update `probabilities` such that each probability distribution
    is normalized (i.e., sums to 1, with relative proportions the same).
    """
    for person in probabilities:
        gene_sum = 0
        for gene_num in probabilities[person]["gene"]:
            gene_sum += probabilities[person]["gene"][gene_num]
        for gene_num in probabilities[person]["gene"]:
            probabilities[person]["gene"][gene_num] = probabilities[person]["gene"][gene_num] / gene_sum

        trait_sum = 0
        for trait in probabilities[person]["trait"]:
            trait_sum += probabilities[person]["trait"][trait]
        for trait in probabilities[person]["trait"]:
            probabilities[person]["trait"][trait] = probabilities[person]["trait"][trait] / trait_sum

    return probabilities


if __name__ == "__main__":
    main()
