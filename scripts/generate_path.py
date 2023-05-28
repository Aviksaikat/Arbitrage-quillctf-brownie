from itertools import permutations, combinations


def generate_path() -> list[list]:
    start_node = "B"
    nodes = ["A", "C", "D", "E"]

    paths = set()

    # Generate combinations of different lengths starting from 1
    for r in range(len(nodes)):
        # Generate combinations without repetition
        for comb in combinations(nodes, r):
            # print(comb)
            # Generate all permutations of the combination
            perms = set(permutations(comb))

            # Generate paths with the start node and permutations
            for perm in perms:
                paths.add(tuple([start_node] + list(perm)))

    # Add individual nodes
    for node in nodes:
        paths.add((start_node, node))

    l = []
    # Print all paths
    for path in paths:
        # print(list(path))
        l.append(path)
    return l


if __name__ == "__main__":
    print(generate_path())
