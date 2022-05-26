"""
PageRank project

week2 project for 'cs50 introduction to artificial intelligence'
https://cs50.harvard.edu/ai/2020/projects/2/pagerank/
"""

import math
import os
import random
import re
import sys

DAMPING = 0.85
SAMPLES = 10000


def main():
    if len(sys.argv) != 2:
        sys.exit("Usage: python pagerank.py corpus")
    corpus = crawl(sys.argv[1])
    ranks = sample_pagerank(corpus, DAMPING, SAMPLES)
    print(f"PageRank Results from Sampling (n = {SAMPLES})")
    for page in sorted(ranks):
        print(f"  {page}: {ranks[page]:.4f}")
    ranks = iterate_pagerank(corpus, DAMPING)
    print(f"PageRank Results from Iteration")
    for page in sorted(ranks):
        print(f"  {page}: {ranks[page]:.4f}")


def crawl(directory):
    """
    Parse a directory of HTML pages and check for links to other pages.
    Return a dictionary where each key is a page, and values are
    a list of all other pages in the corpus that are linked to by the page.
    """
    pages = dict()

    # Extract all links from HTML files
    for filename in os.listdir(directory):
        if not filename.endswith(".html"):
            continue
        with open(os.path.join(directory, filename)) as f:
            contents = f.read()
            links = re.findall(r"<a\s+(?:[^>]*?)href=\"([^\"]*)\"", contents)
            pages[filename] = set(links) - {filename}

    # Only include links to other pages in the corpus
    for filename in pages:
        pages[filename] = set(
            link for link in pages[filename]
            if link in pages
        )

    return pages


def transition_model(corpus, page, damping_factor):
    """
    Return a probability distribution over which page to visit next,
    given a current page.

    With probability `damping_factor`, choose a link at random
    linked to by `page`. With probability `1 - damping_factor`, choose
    a link at random chosen from all pages in the corpus.
    """
    # TODO
    # If page has at least one outgoing link
    if corpus[page]:
        # Shared probability for each page in corpus is: (1 - damping_factor) / num_pages_in_corpus
        shared_probabilities = [(1 - damping_factor) / len(corpus)] * len(corpus)
    # Else if page has no outgoing links
    else:
        # shared probability for each page in corpus is: 1 / num_pages_in_corpus
        shared_probabilities = [1 / len(corpus)] * len(corpus)

    model = dict(zip(corpus.keys(), shared_probabilities))

    if corpus[page]:
        outgoing_link_probability = damping_factor / len(corpus[page])
        # For each outgoing link in current page (if there are any)
        for outgoing_link in corpus[page]:
            # the probability of reaching that page would be: damping_factor / num_outgoing_links_from_current_page
            model[outgoing_link] += outgoing_link_probability

    return model


def sample_pagerank(corpus, damping_factor, n):
    """
    Return PageRank values for each page by sampling `n` pages
    according to transition model, starting with a page at random.

    Return a dictionary where keys are page names, and values are
    their estimated PageRank value (a value between 0 and 1). All
    PageRank values should sum to 1.
    """
    # TODO
    # Initialise pagerank dictionary with all values set to zero
    pageranks = dict(zip(corpus.keys(), [0] * len(corpus)))

    # Start on a random page with equal probability
    page = random.choice(list(corpus.keys()))

    # For each of the remaining samples, the next sample should be generated from the previous sample based on the
    # previous sample’s transition model.
    for _ in range(n):
        pageranks[page] += 1
        model = transition_model(corpus, page, damping_factor)
        page = random.choices(list(model.keys()), weights=list(model.values()))[0]

    # For each page, divide the number of times it was visited (sampled) by n
    pageranks = {page: times_sampled / n for page, times_sampled in pageranks.items()}

    # sum_probs = 0
    # for _, prob in pageranks.items():
    #     sum_probs += prob
    # print("Sum of Pagerank probabilities: ", sum_probs)

    return pageranks


def iterate_pagerank(corpus, damping_factor):
    """
    Return PageRank values for each page by iteratively updating
    PageRank values until convergence.

    Return a dictionary where keys are page names, and values are
    their estimated PageRank value (a value between 0 and 1). All
    PageRank values should sum to 1.
    """
    num_pages = len(corpus)
    pageranks = dict(zip(corpus.keys(), [1 / num_pages] * num_pages))
    pagerank_changes = dict(zip(corpus.keys(), [math.inf] * num_pages))

    num_iterations = 0
    # Update Pagerank values while the change in any updating Pagerank is > 0.001 between iterations
    # Note that at pagerank_change > 0.001, this only undergoes roughly 10 iterations for a corpus of 8 pages, which is
    # not enough for the pagerank values to converge at their true value, so the sum of the Pagerank probabilities is
    # 1.008... (not exactly 1.0 to 3 decimal places).
    while any(pagerank_change > 0.001 for pagerank_change in pagerank_changes.values()):
        num_iterations += 1
        for page in pageranks.keys():
            sum_linked_pageranks = 0
            for link_page, links in corpus.items():
                if not links:
                    links = corpus.keys()
                if page in links:
                    sum_linked_pageranks += pageranks[link_page] / len(links)
            new_pagerank = ((1 - damping_factor) / num_pages) + (damping_factor * sum_linked_pageranks)

            # keep track of change between old and new pageranks
            pagerank_changes[page] = abs(new_pagerank - pageranks[page])
            pageranks[page] = new_pagerank

    # sum_probs = 0
    # for _, prob in pageranks.items():
    #     sum_probs += prob
    # print(f"Sum of Pagerank probabilities: {sum_probs} (n = {num_iterations})")

    return pageranks


if __name__ == "__main__":
    main()
