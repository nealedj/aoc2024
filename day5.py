import copy
from typing import Tuple


def part1():
    print('Day 5 Part 1 of Advent of Code!')

    raw_data = read_raw()
    ordering_rules, updates = read_input(raw_data)

    filtered_updates = [update for update in updates if is_in_order(ordering_rules, update)]

    mids = [update[len(update) // 2] for update in filtered_updates]
    print('Sum of mids:', sum(mids))


def part2():
    print('Day 5 Part 2 of Advent of Code!')

    raw_data = read_raw()
    ordering_rules, updates = read_input(raw_data)

    unordered_updates = [update for update in updates if not is_in_order(ordering_rules, update)]

    sorted_updates = [sort_update(ordering_rules, copy.deepcopy(update)) for update in unordered_updates]

    mids = [update[len(update) // 2] for update in sorted_updates]
    print('Sum of mids:', sum(mids))


def is_in_order(ordering_rules: list, update: list) -> list:
    print('Filtering update:', update)

    out_of_order = False
    for (page1, page2) in ordering_rules:
        if page1 in update and page2 in update:
            index1 = update.index(page1)
            index2 = update.index(page2)

            if index1 > index2:
                out_of_order = True

    return not out_of_order


def sort_update(ordering_rules: list, update: list) -> list:
    print('Sorting update:', update)

    while True:
        swapped = False
        for (page1, page2) in ordering_rules:
            if page1 in update and page2 in update:
                index1 = update.index(page1)
                index2 = update.index(page2)

                if index1 > index2:
                    update[index1] = page2
                    update[index2] = page1
                    swapped = True
        if not swapped:
            break

    print('Sorted update:', update)
    
    return update


def read_input(raw_data: list) -> Tuple[set, list]:
    ordering_rules = set()
    updates = []

    for line in raw_data:
        if ',' in line:
            update = [int(s) for s in line.split(',') if s.isdigit()]
            updates.append(update)
        elif '|' in line:
            rule = tuple(int(s) for s in line.split('|') if s.isdigit())
            ordering_rules.add(rule)

    return ordering_rules, updates


def read_raw() -> list:
    with open('./inputs/day5') as f:
        return [line.strip() for line in f.readlines()]

if __name__ == '__main__':
    part1()
    part2()
