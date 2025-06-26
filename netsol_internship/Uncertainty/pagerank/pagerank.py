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

    distribution = dict()
    N = len(corpus)
    links = corpus[page]

    # If the page has no outgoing links, treat it as linking to all pages (including itself)
    if not links:
        for p in corpus:
            distribution[p] = 1 / N
        return distribution

    for p in corpus:
        # Base probability: random jump to any page
        probability = (1 - damping_factor) / N
        # If p is a linked page, add share of damping factor
        if p in links:
            probability += damping_factor / len(links)
        distribution[p] = probability

    return distribution



import random

def sample_pagerank(corpus, damping_factor, n):
    """
    Return PageRank values for each page by sampling `n` pages
    according to transition model, starting with a page at random.

    Return a dictionary where keys are page names, and values are
    their estimated PageRank value (a value between 0 and 1). All
    PageRank values should sum to 1.
    """

    # 1. Initialize visit counter for each page
    visit_count = {page: 0 for page in corpus}

    # 2. Start with a random page
    pages = list(corpus.keys())
    page = random.choice(pages)
    visit_count[page] += 1

    # 3. Generate n - 1 samples
    for _ in range(n - 1):
        # Get the transition model for the current page
        model = transition_model(corpus, page, damping_factor)
        # Choose the next page according to the transition probabilities
        next_page = random.choices(
            population=list(model.keys()),
            weights=list(model.values()),
            k=1
        )[0]
        visit_count[next_page] += 1
        page = next_page

    # 4. Normalize the counts to get PageRank values
    pagerank = {page: visit_count[page] / n for page in corpus}

    return pagerank



def iterate_pagerank(corpus, damping_factor):
    """
    Return PageRank values for each page by iteratively updating
    PageRank values until convergence (when no PageRank changes by more than 0.001).

    Return a dictionary where keys are page names, and values are
    their estimated PageRank value (a value between 0 and 1). All
    PageRank values should sum to 1.
    """

    N = len(corpus)
    pagerank = {page: 1 / N for page in corpus}  # 1. Initialize PageRanks
    threshold = 0.001
    change = float("inf")

    # Precompute pages that link to each page
    incoming_links = {page: set() for page in corpus}
    for page in corpus:
        for linked_page in corpus[page]:
            if linked_page in corpus:
                incoming_links[linked_page].add(page)
        # Handle dead ends as linking to all pages
        if not corpus[page]:
            for other in corpus:
                incoming_links[other].add(page)

    # 2. Repeat until PageRanks converge
    while change > threshold:
        new_pagerank = {}
        change = 0
        for page in corpus:
            # First part: random jump
            new_rank = (1 - damping_factor) / N

            # Second part: get shares from all pages that link to this page
            for linker in incoming_links[page]:
                num_links = len(corpus[linker]) if corpus[linker] else N
                new_rank += damping_factor * (pagerank[linker] / num_links)

            # Record new rank and track max change
            new_pagerank[page] = new_rank
            change = max(change, abs(new_pagerank[page] - pagerank[page]))

        pagerank = new_pagerank

    # Optional: Normalize (usually already sums to 1)
    total = sum(pagerank.values())
    for page in pagerank:
        pagerank[page] /= total

    return pagerank


if __name__ == "__main__":
    main()
