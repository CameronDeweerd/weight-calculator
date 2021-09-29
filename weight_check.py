from itertools import combinations, product
from collections import Counter

BAR = 45
WEIGHT_LIST = [45, 35, 25, 10, 10, 5, 5, 2.5]


# takes a party of people and splits them into groups to minimize the number of swaps for the overall group
# Group sizes are only 2 or 3
def make_groups(targets):

    best_options = {}
    num_groups = (len(targets)+2)//3    # number of groups assuming only size 2 or 3 allowed
    weight_combos = weight_combination_generator()

    # since there are multiple ways to make a target (35+10 vs 45) we find the best weight combination
    # for a every size 2 and size 3 permutation and put into a dictionary
    size_three = set(combinations(targets, 3))
    size_two = set(combinations(targets, 2))
    for target in size_two:
        best_options[target] = find_best_weight([*target], weight_combos)
    for target in size_three:
        best_options[target] = find_best_weight([*target], weight_combos)

    # generate a list of all parties and then trim it down to only the legal parties
    partitions = sorted_k_partitions(targets, num_groups)  # generate a list of all parties
    final_partition = []
    for i in range(len(partitions)):
        for j in range(num_groups):
            if len(partitions[i][j]) > 3 or len(partitions[i][j]) < 2:  # throw away if not groups of size 2 and size 3
                break
        else:
            final_partition.append(partitions[i])

    # for every party sum up the num of swaps for each of its groups and track the one with the best total
    best_final_group = None
    for group in final_partition:
        num_swaps = 0
        for i in range(num_groups):
            num_swaps = num_swaps + best_options[group[i]][1]

        if not best_final_group:
            best_final_group = group, num_swaps
        elif best_final_group[1] > num_swaps:
            best_final_group = group, num_swaps

    return best_final_group, best_options


# Make a dictionary of all the ways to create a certain number
def weight_combination_generator():
    weight_combos = dict()

    # make a set of all combinations and then just add them up to see what weight they make
    # store this data in a dictionary and append each new value using the target weight as a key
    for i in range(len(WEIGHT_LIST)):
        comboList = set(combinations(WEIGHT_LIST, i + 1))
        for j in comboList:
            if sum(j) in weight_combos:
                weight_combos[sum(j)] = [*weight_combos[sum(j)], j]
            else:
                weight_combos[sum(j)] = [j]

    return weight_combos


# for 2 or 3 targets, find the best combination of weights to minimize swaps
def find_best_weight(targets, weight_combos):
    # covert to one_sided_targets
    targets = check_possible(targets)
    for i in range(len(targets)):
        targets[i] = (targets[i] - 45)/2

    # create a list of permutations of the different ways to make given weight targets
    weight_combos_by_target = []
    for i in targets:
        # print(len(weight_combos[i]), "options to make", i, *weight_combos[i])
        weight_combos_by_target.append(weight_combos[i])  # [[all ways to make target 1], [all ways to make target 2], ...]
    c = list(product(*weight_combos_by_target))

    # find the best combo
    best = None
    for combo in c:
        # make counter dicts for each option and then append the start because its a cycle
        targetCount = []
        for i in range(len(targets)):
            targetCount.append(Counter(combo[i]))
        targetCount.append(Counter(combo[0]))

        # calculate the number of changes required for a given combo and keep track of the best
        # remove all elements in the first target from the next and count the differences
        # then do it again but in reverse because negatives are ignored when we list differences
        dif = 0
        for i in range(len(targets)):
            dif = dif + len(sorted((targetCount[i] - targetCount[i+1]).elements()))
            dif = dif + len(sorted((targetCount[i+1] - targetCount[i]).elements()))
        if not best:
            best = combo, dif
        elif best[1] > dif:
            best = combo, dif

    return best


# changes the targets to be multiples of 5 and between BAR and MAX_WEIGHT
def check_possible(targets):
    MAX_WEIGHT = sum(WEIGHT_LIST) * 2 + BAR

    for i in range(len(targets)):
        if targets[i] < BAR:
            targets[i] = BAR
        if targets[i] > MAX_WEIGHT:
            targets[i] = MAX_WEIGHT
        if not targets[i] % 5 == 0:
            targets[i] = targets[i]//5 * 5

    return targets


def sorted_k_partitions(seq, k):
    """Returns a list of all unique k-partitions of `seq`.

    Each partition is a list of parts, and each part is a tuple.

    The parts in each individual partition will be sorted in short-lex
    order (i.e., by length first, then lexicographically).

    The overall list of partitions will then be sorted by the length
    of their first part, the length of their second part, ...,
    the length of their last part, and then lexicographically.
    """
    n = len(seq)
    groups = []  # a list of lists, currently empty

    def generate_partitions(i):
        if i >= n:
            yield list(map(tuple, groups))
        else:

            if n - i > k - len(groups):
                for group in groups:
                    group.append(seq[i])
                    yield from generate_partitions(i + 1)
                    group.pop()


            if len(groups) < k:
                groups.append([seq[i]])
                yield from generate_partitions(i + 1)

                groups.pop()

    result = generate_partitions(0)

    # Sort the parts in each partition in short-lex order
    result = [sorted(ps, key=lambda p: (len(p), p)) for ps in result]
    # Sort partitions by the length of each part, then lexicographically.
    result = sorted(result, key=lambda ps: (*map(len, ps), ps))

    return result


def main(targets=[100, 140, 150]):
    targets = []

    while True:
        i = input("Enter the next weight target: ")
        if i.isnumeric():
            targets.append(int(i))
            print("current weights: {}".format(targets))
        else:
            break

    final_group, final_options = make_groups(targets)
    print("The best combination is {} with {} swaps required".format(final_group[0], final_group[1]))
    for i in final_group[0]:
        print("Group: {} -> {} with {} swaps".format(i, *final_options[i], final_options[i][1]))

main()
