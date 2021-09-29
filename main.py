# given a set of weights calculate all possiblities of generating a target weight
import weight_check


def main():
    targets = [100, 140, 150]
    final_group, final_options = weight_check.make_groups(targets)
    print("The best combination is {} with {} swaps required".format(final_group[0], final_group[1]))
    for i in final_group[0]:
        print("Group: {} -> {} with {} swaps".format(i, *final_options[i], final_options[i][1]))


main()


