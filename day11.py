
def part1():
    stones = read_input()
    blinks = 25

    for i_blink in range(1, blinks+1):
        print("Blink", i_blink)
        i = 0
        for i in range(0, len(stones)):
            s = str(stones[i])
            l = len(s)
            if stones[i] == 0:
                stones[i] = 1
            elif l % 2 == 0:
                stones[i] = (int(s[:l // 2]), int(s[l // 2:]),)
            else:
                stones[i] *= 2024

            i += 1

        new_stones = [
            stone for value in
            stones for stone in (value if isinstance(value, tuple) else [value])
        ]
        stones = new_stones

    print("Count of stones:", len(stones))


def part2():
    stones = read_input()
    blinks = 75

    cache = {}
    def walk(stone, depth):
        key = (stone, depth,)
        if key in cache:
            return cache[key]

        str_stone = str(stone)
        num_digits = len(str_stone)

        if depth == 0:
            cache[key] = 1
        elif stone == 0:
            cache[key] = walk(1, depth - 1)
        elif num_digits % 2 == 0:
            cache[key] = (
                walk(int(str_stone[:num_digits // 2]), depth-1) +
                     walk(int(str_stone[num_digits // 2:]), depth-1)
            )
        else:
            cache[key] = walk(stone * 2024, depth-1)

        return cache[key]

    count_of_stones = sum(walk(stone, blinks) for stone in stones)

    print("Count of stones:", count_of_stones)


def read_input() -> list:
    with open("./inputs/day11") as f:
        return [int(s) for s in f.read().split(" ")]

if __name__ == "__main__":
    part1()
    part2()
