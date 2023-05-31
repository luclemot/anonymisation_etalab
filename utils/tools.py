from itertools import combinations


def col_set(input):
    """Creates a list of all combinations of elements from input."""
    return sum(
        [list(map(list, combinations(input, i))) for i in range(len(input) + 1)], []
    )
